import cv2
import numpy as np
import matplotlib.pyplot as plt


def find_spectrum_line(frame, region_of_interest):
    roi = frame[region_of_interest[1]:region_of_interest[3],
                region_of_interest[0]:region_of_interest[2]]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    intensity = np.mean(gray_roi, axis=0)
    return intensity


def map_pixels_to_wavelengths(intensity, wavelength_range=(400, 700)):
    num_pixels = len(intensity)
    wavelengths = np.linspace(wavelength_range[0], wavelength_range[1], num_pixels)
    return wavelengths


def main():
    camera_index = 1
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Error: Unable to access the camera")
        return

    # Initialization
    I0 = None  # Reference intensity
    wavelength_range = (400, 700)  # Wavelength range in nm
    roi_coordinates = (100, 200, 600, 250)  # (x1, y1, x2, y2)

    # Constants for Beer-Lambert law
    epsilon = 0.02  # Molar absorptivity (example value in L·mol^-1·cm^-1)
    path_length = 1  # Path length (cm)

    print("Press 'r' to record reference intensity (I0)")
    print("Press 'q' to quit")

    plt.ion()  # Enable interactive mode for real-time plotting
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture frame")
            break

        # Draw the ROI on the live feed
        cv2.rectangle(frame, (roi_coordinates[0], roi_coordinates[1]),
                      (roi_coordinates[2], roi_coordinates[3]), (0, 255, 0), 2)

        # Extract the intensity profile
        intensity = find_spectrum_line(frame, roi_coordinates)
        wavelengths = map_pixels_to_wavelengths(intensity, wavelength_range)

        if I0 is None:
            # Plot the intensity spectrum with colors
            plt.clf()
            plt.scatter(wavelengths, intensity, c=wavelengths, cmap='rainbow', s=5)
            plt.colorbar(label='Wavelength (nm)')
            plt.xlabel('Wavelength (nm)')
            plt.ylabel('Intensity')
            plt.title('Real-Time Intensity Spectrum (Colorful)')
            plt.pause(0.001)
        else:
            # Calculate absorbance
            absorbance = -np.log10(intensity / I0)
            absorbance = np.clip(absorbance, 0, np.inf)  # Avoid invalid values

            # Calculate concentration using Beer-Lambert law
            concentration = absorbance / (epsilon * path_length)
            mean_concentration = np.mean(concentration)/10  # Average concentration

            # Plot absorbance spectrum
            plt.clf()
            plt.subplot(211)
            plt.scatter(wavelengths, absorbance, c=wavelengths, cmap='viridis', s=5)
            plt.colorbar(label='Wavelength (nm)')
            plt.xlabel('Wavelength (nm)')
            plt.ylabel('Absorbance')
            plt.title('Real-Time Absorbance Spectrum')

            # Plot mean concentration
            plt.subplot(212)
            plt.axhline(mean_concentration, color='red', linestyle='--', label=f'Mean Concentration = {mean_concentration:.3f} mol/L')
            plt.xlabel('Wavelength (nm)')
            plt.ylabel('Concentration (mol/L)')
            plt.title('Real-Time Concentration')
            plt.legend()

            plt.pause(0.001)

            # Display mean concentration in terminal
            print(f"Mean Concentration: {mean_concentration:.3f} mol/L")

        # Show the live webcam feed
        cv2.imshow('Spectrometer View', frame)

        # Handle key events
        key = cv2.waitKey(1) & 0xFF
        if key == ord('r'):
            I0 = intensity.copy()  # Record reference intensity
            print("Reference intensity (I0) recorded successfully")
        elif key == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    plt.close()



main()