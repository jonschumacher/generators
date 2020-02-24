
package org.eclipse.smarthome.binding.tinkerforge.internal;

import java.net.URL;
import java.util.Collections;
import java.util.HashSet;
import java.util.Locale;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

import org.eclipse.smarthome.binding.tinkerforge.internal.device.DeviceWrapperFactory;

import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.jetty.client.HttpClient;
import org.eclipse.jetty.client.api.Result;
import org.eclipse.jetty.client.util.BufferingResponseListener;
import org.eclipse.smarthome.core.common.ThreadPoolManager;
import org.eclipse.smarthome.core.thing.Thing;
import org.eclipse.smarthome.core.thing.ThingTypeUID;
import org.eclipse.smarthome.core.thing.binding.firmware.Firmware;
import org.eclipse.smarthome.core.thing.binding.firmware.FirmwareBuilder;
import org.eclipse.smarthome.core.thing.firmware.FirmwareProvider;
import org.eclipse.smarthome.io.net.http.HttpClientFactory;
import org.eclipse.smarthome.io.net.http.HttpUtil;
import org.osgi.service.component.annotations.Component;
import org.osgi.service.component.annotations.Reference;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Component(service = FirmwareProvider.class)
public class TinkerforgeFirmwareProvider implements FirmwareProvider {
    private HttpClient httpClient;

    private final Logger logger = LoggerFactory.getLogger(TinkerforgeChannelTypeProvider.class);

    private class FirmwareInfo {
        public FirmwareInfo(String version, String url) {
            this.version = version;
            this.url = url;

        }
        String version;
        String url;
    }

    private final ConcurrentMap<String, FirmwareInfo> latestVersions = new ConcurrentHashMap<>();

    protected final ScheduledExecutorService scheduler = ThreadPoolManager.getScheduledPool("tinkerforge-firmware");

    @Override
    public Firmware getFirmware(Thing thing, String version) {
        return getFirmware(thing, version, null);
    }

    @Nullable
    @Override
    public Firmware getFirmware(Thing thing, String version, @Nullable Locale locale) {
        return getFirmwares(thing, locale).stream().filter(fw -> fw.getVersion().equals(version)).findFirst()
                .orElse(null);
    }

    @Override
    public Set<Firmware> getFirmwares(Thing thing) {
        return getFirmwares(thing, null);
    }

    @Override
    public Set<Firmware> getFirmwares(Thing thing, Locale locale) {
        Set<Firmware> result = new HashSet<>();
        String id = thing.getThingTypeUID().getId();
        FirmwareInfo info = latestVersions.get(id);
        if (info != null)
            result.add(buildFirmware(thing.getThingTypeUID(), info.version, info.url));
        return result;

    }

    private Firmware buildFirmware(ThingTypeUID ttuid, String version, String url) {
        return FirmwareBuilder.create(ttuid, version)
                              .withVendor("Tinkerforge GmbH")
                              .withProperties(Collections.singletonMap(TinkerforgeBindingConstants.PROPERTY_FIRMWARE_URL, url))
                              .build();
    }

    private void parseLatestVersions(String latestVersionsText) {
        for(String line : latestVersionsText.split("\n")) {
            boolean isBrick = line.startsWith("bricks:");
            boolean isBricklet = line.startsWith("bricklets:");
            boolean isExtension = line.startsWith("extensions:");
            if (!(isBrick || isBricklet || isExtension))
                continue;

            String[] splt = line.split(":");
            String deviceType = splt[0].substring(0, splt[0].length() - 1);
            String deviceName = splt[1];
            String thingName = deviceType + deviceName.replace("_", "");

            if(deviceName.equals("hat") || deviceName.equals("hat_zero"))
                thingName = "brick" + deviceName.replace("_", "");

            if(deviceName.contains("lcd_20x4_v1"))
                thingName = deviceType + "lcd20x4";

            String version = splt[2];
            boolean isCoMCU = isExtension || DeviceWrapperFactory.getDeviceInfo(thingName).isCoMCU;
            String urlString = String.format(
                "https://download.tinkerforge.com/firmwares/%s/%s/%s_%s_firmware_%s.%s",
                deviceType + 's', deviceName,
                deviceType, deviceName,
                version.replace(".", "_"),
                isCoMCU ? "zbin" : "bin");

            latestVersions.put(thingName, new FirmwareInfo(version, urlString));
        }
    }

    private void getLatestVersions() {
        if (this.httpClient == null)
            return;

        this.httpClient
            .newRequest("https://download.tinkerforge.com/latest_versions.txt")
            .send(new BufferingResponseListener() {
                @Override
                public void onComplete(Result result) {
                    if (result.isSucceeded()) {
                        parseLatestVersions(getContentAsString());
                        scheduler.schedule(() -> getLatestVersions(), 1, TimeUnit.HOURS);
                    } else {
                        logger.info("Failed to download latest versions: {}", result.getFailure().toString());
                        scheduler.schedule(() -> getLatestVersions(), 5, TimeUnit.MINUTES);
                    }
                }
            });
    }

    @Reference
    protected void setHttpClientFactory(HttpClientFactory httpClientFactory) {
        this.httpClient = httpClientFactory.createHttpClient("tinkerforge");
        try {
            this.httpClient.start();
        } catch (Exception e) {
            logger.info("Failed to start HTTP Client: {}", e.getMessage());
            return;
        }
        getLatestVersions();
    }

    protected void unsetHttpClientFactory(HttpClientFactory httpClientFactory) {
        try {
            this.httpClient.stop();
        } catch (Exception e) {
            logger.info("Failed to stop HTTP Client: {}", e.getMessage());
        }
        this.httpClient = null;
    }
}
