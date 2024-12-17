import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mcollections
import tkinter as tk
from tkinter import filedialog

def find_spectrum_line(frame):
    """
    Extracts the intensity profile along a horizontal line across the entire frame.
    """
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    intensity = np.mean(gray_frame, axis=0)
    return intensity

def map_pixels_to_wavelengths(intensity, wavelength_range=(380, 1200)):
    """
    Maps pixel positions in the intensity profile to wavelengths in the specified range.
    """
    num_pixels = len(intensity)
    wavelengths = np.linspace(wavelength_range[0], wavelength_range[1], num_pixels)
    return wavelengths

camera_index = 1  # Update this index based on your camera setup
cap = cv2.VideoCapture(camera_index)

if not cap.isOpened():
    print("Error: Unable to access the camera")

# Add before the main loop
wavelength_accumulator = []
intensity_accumulator = []

# Parameters
wavelength_range = (300, 1200)  # Wavelength range in nm
# Define the wavelength range for visible spectrum
visible_min, visible_max = 380, 750

print("Press 'q' to quit")

plt.ion()  # Enable interactive mode for real-time plotting

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture frame")
            break

        # Extract the intensity profile
        intensity = find_spectrum_line(frame)
        wavelengths = map_pixels_to_wavelengths(intensity, wavelength_range)
        
        # Accumulate data
        wavelength_accumulator.append(wavelengths)
        intensity_accumulator.append(intensity)
        
        # Find indices for UV and IR wavelengths
        uv_indices = [i for i, x in enumerate(wavelengths) if x >= wavelength_range[0] and x < visible_min]
        ir_indices = [i for i, x in enumerate(wavelengths) if x > visible_max and x <= wavelength_range[1]]
        visible_indices = [i for i, x in enumerate(wavelengths) if x >= visible_min and x <= visible_max]

        # Extract corresponding intensities
        uv_wavelengths = wavelengths[uv_indices]
        uv_intensities = intensity[uv_indices]

        ir_wavelengths = wavelengths[ir_indices]
        ir_intensities = intensity[ir_indices]
        
        visible_wavelengths = wavelengths[visible_indices]
        visible_intensities = intensity[visible_indices]

        plt.clf()
        # plt.plot(wavelengths, intensity, color='black', linewidth=1, zorder=1)  # Thin black line
        
        points = np.array([visible_wavelengths, visible_intensities]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        lc = mcollections.LineCollection(segments, cmap='rainbow', 
                                        norm=plt.Normalize(visible_wavelengths.min(), visible_wavelengths.max()))
        lc.set_array(visible_wavelengths)
        lc.set_linewidth(2)
        plt.gca().add_collection(lc)
        
        plt.plot(uv_wavelengths, uv_intensities, color='black', linewidth=1, zorder=1)
        plt.plot(ir_wavelengths, ir_intensities, color='black', linewidth=1, zorder=1)
        
        # Create scatter plot with custom colormap
        scatter = plt.scatter(wavelengths, intensity, c=wavelengths, cmap='rainbow', vmin=visible_min, vmax=visible_max, s=5, zorder=2)
        plt.colorbar(scatter, label='Wavelength (nm)')
        
        plt.scatter(uv_wavelengths, uv_intensities, color='black', s=5, zorder=2)
        plt.scatter(ir_wavelengths, ir_intensities, color='black', s=5, zorder=2)
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Intensity')
        plt.title('Real-Time Intensity Spectrum')
        plt.pause(0.001)

        # Show the live webcam feed
        cv2.imshow('Spectrometer View', frame)

        # Handle key events
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

finally:
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    plt.close()
    
    # Prompt for file saving
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Open file dialog to choose save location
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        title="Save Spectrum Data"
    )
    
    # Save data if a file path is selected
    if file_path:
        # Calculate time-averaged wavelengths and intensities
        avg_wavelengths = np.mean(wavelength_accumulator, axis=0)
        avg_intensities = np.mean(intensity_accumulator, axis=0)
        
        # Create a formatted array for saving
        data = np.column_stack((avg_wavelengths, avg_intensities))
        
        # Save to file with formatted header
        np.savetxt(file_path, data, 
                   header='  nm\t\t\tI', 
                   fmt='%.2f\t\t%.5f', 
                   comments='')
        
        print(f"Spectrum data saved to {file_path}")