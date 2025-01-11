# GeoSleuth 🚀

GeoSleuth is a Python script that allows you to extract the location of a device with superior accuracy by leveraging Google services, rather than relying on IP-based geolocation methods. This approach is more accurate and reliable, as it uses actual device location data instead of approximate IP geolocation.

## Features 💡

- **Accurate Location Extraction**: Extract the exact location using Google services.
- **Custom EXE Builder**: Create a custom executable or Python script with various configuration options.
- **Silent Mode**: Run the script silently in the background without any window showing.
- **Address Option**: Get the full address along with the location.
- **Accuracy Measurement**: Get the location accuracy in meters (as a radius).
- **Flexible Configuration**: Choose different options like debug mode and custom builds.

## Installation 💻

```bash
git clone https://github.com/Synthiny/GeoSleuth.git
cd geosleuth
pip install -r requirements.txt
```

## Requirements 🔑

Before you can use GeoSleuth, you'll need an internet connection and the necessary Python dependencies installed. Make sure to install the required libraries using the command:

```bash
pip install -r requirements.txt
```

## Usage 📚

To run GeoSleuth and extract location, simply use:

```bash
python geosleuth.py -run -debug
```

You can customize the output with various options:

- **Get Address**: Returns the address instead of longitude/latitude.
  ```bash
  python geosleuth.py -run -address
  ```

- **Enable Debug Mode**: Displays detailed logs for debugging.
  ```bash
  python geosleuth.py -run -debug
  ```

- **Silent Mode**: Runs silently in the background without showing any windows.
  ```bash
  python geosleuth.py -run -nowindow
  ```

- **Display Accuracy**: Shows the location's accuracy (in meters as a radius).
  ```bash
  python geosleuth.py -run -accuracy
  ```

- **Build Custom EXE/Python File**: Enter build mode to create a custom executable or Python script.
  ```bash
  python geosleuth.py -build
  ```

## Build Mode Configuration ⚙️

After running the `-build` command, GeoSleuth will prompt you to configure the following options:

1. **NoWindow**: Specify if the build should run without a window.
2. **Debug**: Enable or disable debug mode for troubleshooting.
3. **Address**: Decide whether to include address information in the output.
4. **Accuracy**: Return the accuracy of the geolocation (in meters as a radius).
5. **System Check**: Option to include tracker files to prevent the script from ever running again (not recommended).
6. **Webhook**: Gives the user the option to relay the extracted info to a discord webhook.
   

## Examples:

- Extract location with address and accuracy:
  ```bash
  python geosleuth.py -run -address -accuracy
  ```

- Build a custom EXE or Python script:
  ```bash
  python geosleuth.py -build
  ```

- Run silently in the background:
  ```bash
  python geosleuth.py -run -nowindow
  ```

## Why GeoSleuth is More Accurate than IP Geolocation Services 🌍

GeoSleuth is more accurate than traditional IP-based geolocation because:

- **Device-based Geolocation**: It uses the device's actual location data through Google services, which provides real-time and precise positioning.
- **Less Reliance on IP Data**: IP-based geolocation can be unreliable, as it uses the IP address of the device, which can be easily spoofed or inaccurate.
- **GPS and Other Sensor Data**: Google services often leverage GPS, Wi-Fi, and other sensors to refine location accuracy.

## Disclaimer ⚠️

Use this tool responsibly. Ensure that you have permission to gather location data from the device. The author is not responsible for any misuse of this software.
