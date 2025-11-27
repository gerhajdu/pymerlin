# PyMERLIN: Metallicity Estimate of Rr Lyrae In the Near-infrared

This routine estimates the iron abundance of RR Lyrae variables from their K-band light curve parameters,
as determined by the PyFiNeR routine (https://github.com/gerhajdu/pyfiner). These estimates are described
in detail in [Hajdu et al. (2018)](https://arxiv.org/abs/1804.01456).

This routine was developed for:
- `Python` 2.7+ or 3.6+
- `Numpy` 1.12+
- `Scikit-learn` 0.19.1

## Installation

Copy all files from the `bin` directory to the same directory in the system PATH.
If you get "ImportError: No module named builtins" error while using Python 2.7,
install the `future` package.
Note that the code relies on loading a pre-trained regressor object, which might
not load if using a `Sklearn` version other than 0.19.1. It is recommended to run
this code from a virtual environment with `python`==3.6, `numpy`==1.12 and
`scikit-learn`==0.19.1 .

## Usage

The only argument the program expects is the location of a file, containing at least six columns,
where the first six columns should be:
- NAME: the name of the variable
- PERIOD: the period determined by the PyFiNeR routine
- U1..U4: the amplitudes of the K-band principal components fit to the light curve by the PyFiNeR routine

Given these data, the code calculates the Fourier parameters used during the regression, imports
the regressors from the attached pickle file, and calculates the abundance estimates on both the
Jurcsik (1995) and the Carretta et al. (2009) metallicity scales, as described in
[Hajdu et al. (2018)](https://arxiv.org/abs/1804.01456).

The output produced by the routine is:
- NAME: the name of the variable
- [Fe/H]_J95: the estimated iron abundance on the Jurcsik (1995) scale
- [Fe/H]_J95: the error from the standard deviation of the 100 separate estimates given by the
regressors on the Jurcsik (1995) scale
- [Fe/H]_C09: the estimated iron abundance on the Carretta et al. (2009) scale
- [Fe/H]_C09: the error from the standard deviation of the 100 separate estimates given by the
regressors on the Carretta et al. (2009) scale
