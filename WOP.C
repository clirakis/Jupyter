{
    // test of wire over groundplane
    Double_t u0      = 4.0e-7 * TMath::Pi();  // H/m
    Double_t Length  = 50.0;                  // meters
    Double_t Height  =  2.0;                  // meters
    Double_t awg22_D =  0.64516e-3;           // awg 22 in meters

    Double_t L = u0/(2.0*TMath::Pi()) * Length * TMath::ACosH(Height/awg22_D);

    cout << " Inductance: " << L << endl;
}
