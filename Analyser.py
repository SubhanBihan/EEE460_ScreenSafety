import numpy as np
 
# Constants
h = 6.626e-34  # Planck's constant (Js)
c = 3.0e8      # Speed of light (m/s)
e = 1.602e-19  # Joules to eV
 
file_path1 = "C:\\Users\\SBihan\\Desktop\\Theremino\\Spectrum_bg.txt"
file_path2 = "C:\\Users\\SBihan\\Desktop\\Theremino\\Spectrum_v2.txt"
   
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
 
# Example usage:
 
# start_wavelength = 300.0
# end_wavelength = 400.0
# intensity_integral = integrate_intensity(file_path, start_wavelength, end_wavelength)
# print(f"The integral of intensity is: {intensity_integral}")
 
# energy_integral = integrate_photon_energy(file_path, start_wavelength, end_wavelength)
# print(f"The integral of intensity * photon energy is: {energy_integral} eV·nm")
 
"""TO DO:
1. Meet requirements
2. Make some kind of flashy GUI to display assessment
3. NUMBER OF PHOTONS or ENERGY ratio???
"""
 
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
print(f"Display Efficiency: {visible_light_efficiency}%")