import numpy as np
import tkinter as tk
from tkinter import filedialog
 
# Constants
h = 6.626e-34  # Planck's constant (Js)
c = 3.0e8      # Speed of light (m/s)
e = 1.602e-19  # Joules to eV

# Prompt for file opening
root = tk.Tk()
root.withdraw()  # Hide the main window

# Open file dialog to choose a .txt file
file_path1 = filedialog.askopenfilename(
    filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    title="Open Background Spectrum Data"
)

# Prompt for file opening
root = tk.Tk()
root.withdraw()  # Hide the main window

# Open file dialog to choose a .txt file
file_path2 = filedialog.askopenfilename(
    filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    title="Open Source Spectrum Data"
)
   
def integrate_intensity(file_path, start_wavelength, end_wavelength):
    """
    Integrates the intensity with respect to wavelength over a specified range.
 
    Parameters:
        file_path (str): Path to the spectrum data file.
        start_wavelength (float): Start wavelength for integration.
        end_wavelength (float): End wavelength for integration.
 
    Returns:
        float: The calculated integral of intensity.
    """
    
    data = np.loadtxt(file_path, skiprows=1)
   
    # Extract wavelength and intensity columns
    wavelengths = data[:, 0]
    intensities = data[:, 1]
   
    # Filter the data within the desired range
    mask = (wavelengths >= start_wavelength) & (wavelengths <= end_wavelength)
    filtered_wavelengths = wavelengths[mask]
    filtered_intensities = intensities[mask]
   
    # Calculate the integrand: I(lambda) * lambda. h*c is a constant so doesn't matter for ratio
    integrand = filtered_intensities * filtered_wavelengths
   
    # Perform numerical integration using the trapezoidal rule
    integral = np.trapz(integrand, filtered_wavelengths)
   
    return integral
 
def integrate_photon_energy(file_path, start_wavelength, end_wavelength):
    """
    Integrates intensity * photon energy with respect to wavelength over a specified range.
 
    Parameters:
        file_path (str): Path to the spectrum data file.
        start_wavelength (float): Start wavelength for integration (in nm).
        end_wavelength (float): End wavelength for integration (in nm).
 
    Returns:
        float: The calculated integral of intensity * photon energy (in eV·nm).
    """
    
    data = np.loadtxt(file_path, skiprows=1)
   
    # Extract wavelength and intensity columns
    wavelengths = data[:, 0]  # in nm
    intensities = data[:, 1]
   
    # Filter the data within the desired range
    mask = (wavelengths >= start_wavelength) & (wavelengths <= end_wavelength)
    filtered_wavelengths = wavelengths[mask]
    filtered_intensities = intensities[mask]
   
    # Perform numerical integration using the trapezoidal rule
    integral = np.trapz(filtered_intensities, filtered_wavelengths)
   
    return integral
 
visible_light_photons = integrate_intensity(file_path2, 380, 750) - integrate_intensity(file_path1, 380, 750)
visible_light_energy = integrate_photon_energy(file_path2, 380, 750) - integrate_photon_energy(file_path1, 
                                                                                               380, 750)
 
blue_light_photons = integrate_intensity(file_path2, 380, 495) - integrate_intensity(file_path1, 380, 495)
blue_light_energy = integrate_photon_energy(file_path2, 380, 495) - integrate_photon_energy(file_path1, 380, 495)
 
ir_photons = integrate_intensity(file_path2, 750, 1200) - integrate_intensity(file_path1, 750, 1200)
ir_energy = integrate_photon_energy(file_path2, 750, 1200) - integrate_photon_energy(file_path1, 750, 1200)
 
blue_light_perc = 100 * blue_light_energy / visible_light_energy
visible_light_efficiency = 100 * visible_light_energy / (visible_light_energy + ir_energy)
 
print(f"Short-wavelength light percentage (in visible spectrum): {blue_light_perc}%")
if blue_light_energy > 30:
    print("Prolonged Exposure Unsafe!")
else:
    print("Relatively Safe!")
    
print(f"Display Efficiency: {visible_light_efficiency}%")
if visible_light_efficiency > 60:
    print("Acceptable Optical Efficiency!")
else:
    print("Your Display is quite inefficient!")