{
    Double_t F = 1.0e9;
    Double_t omega = 2.0*TMath::Pi()*F;
    Double_t L = 1.0e-9;  // Henries
    Double_t C = 1.0e-12; // Farads
    Double_t XL = omega*L;
    Double_t XC = -1.0/(omega*C);

    Double_t ZI = XL+XC;
    Double_t Z0 = 50.0;
    Double_t ZL = ZI;
    Double_t absZ = sqrt(pow(Z0,2.0)+pow(ZI,2.0));

    /*
     * Gamma = (Z_in - Z0)/(Z_in+Z0)
     * source impedance is 50 ohms resistive
     */
    Double_t Gamma = (absZ-Z0)/(absZ+Z0);

    cout << "Gamma = " << Gamma << endl;

}
