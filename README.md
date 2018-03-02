# PyMERLIN: Metallicity Estimate of Rr Lyrae In the Near-infrared

This routine estimates the iron abundance of RR Lyrae variables from their K-band light curve parameters,
as determined by the PyFiNeR routine (https://github.com/gerhajdu/pyfiner). These estimates are described
in detail in Hajdu et al. (2018).

This routine was developed for:
- `Python` 2.7
- `Numpy` 1.12

## Installation

Copy all files from the `bin` directory to the same directory in the system PATH

## Usage

The only argument the program expects is the location of a file, containing at least six columns,
where the first six columns should be:
- NAME: the name of the variable
- PERIOD: the period determined by the PyFiNeR routine
- U1..U4: the amplitudes of the K-band principal components fit to the light curve by the PyFiNeR routine

Given these data, the code calculates the Fourier parameters used during the regression, imports
the regressors from the attached pickle file, and calculates the abundance estimates on both the
Jurcsik (1995) and the Carretta et al. (2009) metallicity scales, as described in Hajdu et al. (2018).

The output produced by the routine is:
- NAME: the name of the variable
- [Fe/H]_J95: the estimated iron abundance on the Jurcsik (1995) scale
- [Fe/H]_J95: the error from the standard deviation of the 100 separate estimates given by the
regressors on the Jurcsik (1995) scale
- [Fe/H]_C09: the estimated iron abundance on the Carretta et al. (2009) scale
- [Fe/H]_C09: the error from the standard deviation of the 100 separate estimates given by the
regressors on the Carretta et al. (2009) scale
