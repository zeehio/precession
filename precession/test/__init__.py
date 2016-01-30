
import sys,os
import precession 
import numpy
from matplotlib import use #Useful when working on SSH
use('Agg') 
from matplotlib import rc #Set plot defaults
font = {'family':'serif','serif':['cmr10'],'weight' : 'medium','size' : 17}
rc('font', **font)
rc('text',usetex=True)
rc('figure',max_open_warning=1000)
import pylab


def parameter_selection():
    '''
    Selection of consistent parameters to describe the BH spin orientations, both at finite and infinitely large separations. Compute some quantities which characterize the spin-precession dynamics, such as morphology, precessional period and resonant angles.
    All quantities are given in total-mass units c=G=M=1.

    **Run using**

        import precession.test
        precession.test.parameter_selection()
    '''

    print "\n *Parameter selection at finite separation*"
    q=0.8   # Must be q<=1. Check documentation for q=1.
    chi1=1. # Must be chi1<=1
    chi2=1. # Must be chi2<=1
    print "We study a binary with:"
    print "\t mass ratio q= %.3f" %q
    print "\t dimensionless spins chi1=%.3f and chi2=%.3f" %(chi1,chi2)
    M,m1,m2,S1,S2=precession.get_fixed(q,chi1,chi2) # Total-mass units M=1
    print "\t spin magnitudes S1=%.3f and S2=%.3f" %(S1,S2)
    r=100*M # Must be r>10M for PN to be valid
    print "\t separation is r=%.3f" %r
    xi_min,xi_max=precession.xi_lim(q,S1,S2)
    Jmin,Jmax=precession.J_lim(q,S1,S2,r)
    Sso_min,Sso_max=precession.Sso_limits(S1,S2)
    print "The geometrical limits on xi,J and S are"
    print "\t %.3f <= xi <= %.3f" %(xi_min,xi_max)
    print "\t %.3f <= J <= %.3f" %(Jmin,Jmax)
    print "\t %.3f <= S <= %.3f" %(Sso_min,Sso_max)
    J= (Jmin+Jmax)/2.
    print "We select a value of J=%.3f within the limits." %J
    St_min,St_max=precession.St_limits(J,q,S1,S2,r)
    print "This constraints the range of S to"
    print "\t %.3f <= S <= %.3f" %(St_min,St_max)
    xi_low,xi_up=precession.xi_allowed(J,q,S1,S2,r)
    print "The allowed values of xi can be found extremizing the effective potentials"
    print "\t %.3f <= xi <= %.3f" %(xi_low,xi_up)
    xi=(xi_low+xi_up)/2.
    print "We select a value of xi=%.3f within the limits." %xi
    test=(J>=min(precession.J_allowed(xi,q,S1,S2,r)) and J<=max(precession.J_allowed(xi,q,S1,S2,r)))
    print "Is our couple (xi,J) consistent?", test
    Sb_min,Sb_max=precession.Sb_limits(xi,J,q,S1,S2,r)
    print "S oscillates between S-=%.3f and S+=%.3f" %(Sb_min,Sb_max)
    S=(Sb_min+Sb_max)/2.
    print "We select a value of S=%.3f between S- and S+" %S
    t1,t2,dp,t12=precession.parametric_angles(S,J,xi,q,S1,S2,r)
    print "The angles describing the spin orientations are"
    print "\t (theta1,theta2,DeltaPhi)=(%.3f,%.3f,%.3f)" %(t1,t2,dp)
    xi,J,S = precession.from_the_angles(t1,t2,dp,q,S1,S2,r)
    print "From the angles one can go back to (xi,J,S)=(%.3f,%.3f,%.3f)" %(xi,J,S)

    print "\n *Features of spin precession*"
    t1_dp0,t2_dp0,t1_dp180,t2_dp180=precession.resonant_finder(xi,q,S1,S2,r)
    print "The spin-orbit resonances are located at"
    print "\t (theta1,theta2)=(%.3f,%.3f) for DeltaPhi=0" %(t1_dp0,t2_dp0)
    print "\t (theta1,theta2)=(%.3f,%.3f) for DeltaPhi=pi" %(t1_dp180,t2_dp180)
    tau = precession.precession_period(xi,J,q,S1,S2,r)
    print "We integrate dt/dS to calculate the period tau=%.3f" %tau
    alpha = precession.alphaz(xi,J,q,S1,S2,r)
    print "We integrate Omega*dt/dS to find alpha=%.3f" %alpha
    morphology = precession.find_morphology(xi,J,q,S1,S2,r)
    if morphology==-1: labelm="Librating about DeltaPhi=0"
    elif morphology==1: labelm="Librating about DeltaPhi=pi"    
    elif morphology==0: labelm="Circulating"
    print "The precessional morphology of this binary is: "+labelm
    sys.stdout = os.devnull # Ignore warnings
    phase,xi_transit_low,xi_transit_up=precession.phase_xi(J,q,S1,S2,r)
    sys.stdout = sys.__stdout__ # Restore warnings
    if phase==-1: labelp="a single DeltaPhi~pi phase"
    elif phase==2: labelp="two DeltaPhi~pi phases, a Circulating phase"    
    elif phase==3: labelp="a DeltaPhi~0, a Circulating, a DeltaPhi~pi phase"
    print "The coexisintg phases are: "+labelp
    print "Indeed, the current morphology ("+labelm+") is part of those."

    print "\n *Parameter selection at infinitely separation*"
    print "We study a binary with:"
    print "\t mass ratio q= %.3f" %q
    print "\t dimensionless spins chi1=%.3f and chi2=%.3f" %(chi1,chi2)
    print "\t at infinitely large separation"
    kappainf_min,kappainf_max=precession.kappainf_lim(S1,S2)
    print "The geometrical limits on xi and kappa_inf are"    
    print "\t %.3f <= xi <= %.3f" %(xi_min,xi_max)
    print "\t %.3f <= kappa_inf <= %.3f" %(kappainf_min,kappainf_max)
    print "We select a value of xi=%.3f within the limits." %xi
    kappainf_low,kappainf_up=precession.kappainf_allowed(xi,q,S1,S2)
    print "This constraints the range of kappa_inf to"
    print "\t %.3f <= kappa_inf <= %.3f" %(kappainf_low,kappainf_up)
    kappainf=(kappainf_low+kappainf_up)/2.
    print "We select a value of kappa_inf=%.3f within the limits." %kappainf
    test=(xi>=min(precession.xiinf_allowed(kappainf,q,S1,S2)) and xi<=max(precession.xiinf_allowed(kappainf,q,S1,S2)))
    print "Is our couple (xi,kappa_inf) consistent?", test 
    t1_inf,t2_inf=precession.thetas_inf(xi,kappainf,q,S1,S2)
    print "The asymptotic (constant) values of theta1 and theta2 are"
    print "\t (theta1_inf,theta2_inf)=(%.3f,%.3f)" %(t1_inf,t2_inf)
    xi,kappainf = precession.from_the_angles_inf(t1_inf,t2_inf,q,S1,S2)
    print "From the angles one can go back to (xi,kappa_inf)=(%.3f,%.3f)" %(xi,kappainf)


def spin_angles():
    '''
    Binary dynamics on the precessional timescale. The spin angles
    theta1,theta2, DeltaPhi and theta12 are computed and plotted against the
    time variable, which is obtained integrating dS/dt. The morphology is also
    detected as indicated in the legend of the plot. Output is saved in
    ./spin_angles.pdf.

    **Run using**

        import precession.test
        precession.test.spin_angles()
    '''

    fig=pylab.figure(figsize=(6,6)) #Create figure object and axes
    ax_t1=fig.add_axes([0,0.95,0.6,0.8]) #top-left
    ax_t2=fig.add_axes([0.8,0.95,0.6,0.8]) #top-right
    ax_dp=fig.add_axes([0,0,0.6,0.8]) #bottom-left
    ax_t12=fig.add_axes([0.8,0,0.6,0.8]) #bottom-right

    q=0.7   # Mass ratio. Must be q<=1.
    chi1=0.6 # Primary spin. Must be chi1<=1
    chi2=1. # Secondary spin. Must be chi2<=1
    M,m1,m2,S1,S2=precession.get_fixed(q,chi1,chi2) # Total-mass units M=1
    r=20*M # Separation. Must be r>10M for PN to be valid
    J=0.94 # Magnitude of J: Jmin<J<Jmax as given by J_lim
    xi_vals=[-0.41,-0.3,-0.22] # Effective spin: xi_low<xi<xi_up as given by xi_allowed

    for xi,color in zip(xi_vals,['blue','green','red']): # Loop over three binaries

        tau = precession.precession_period(xi,J,q,S1,S2,r) #Period
        morphology = precession.find_morphology(xi,J,q,S1,S2,r) # Morphology
        if morphology==-1: labelm="${\\rm L}0$"
        elif morphology==1: labelm="${\\rm L}\\pi$"   
        elif morphology==0: labelm="${\\rm C}$"
        Sb_min,Sb_max=precession.Sb_limits(xi,J,q,S1,S2,r) # Limits in S
        S_vals = numpy.linspace(Sb_min,Sb_max,1000) # Create array, from S- to S+
        S_go=S_vals # First half of the precession cycle: from S- to S+
        t_go=map(lambda x: precession.t_of_S(S_go[0],x, Sb_min,Sb_max,xi,J,q,S1,S2,r,0,sign=-1),S_go) # Compute time values. Assume t=0 at S-      
        t1_go,t2_go,dp_go,t12_go=zip(*[precession.parametric_angles(S,J,xi,q,S1,S2,r) for S in S_go]) # Compute the angles. Assume DeltaPhi>=0 in the first half of the cycle
        S_back=S_vals[::-1] # Second half of the precession cycle: from S+ to S-
        t_back=map(lambda x: precession.t_of_S(S_back[0],x, Sb_min,Sb_max, xi,J,q,S1,S2,r,t_go[-1],sign=1.),S_back) # Compute time, start from the last point of the first half t_go[-1]
        t1_back,t2_back,dp_back,t12_back=zip(*[precession.parametric_angles(S,J,xi,q,S1,S2,r) for S in S_back]) # Compute the angles.
        dp_back=[-dp for dp in dp_back] # Assume DeltaPhi<=0 in the second half of the cycle

        for ax,vec_go,vec_back in zip([ax_t1,ax_t2,ax_dp,ax_t12], [t1_go,t2_go,dp_go,t12_go], [t1_back,t2_back,dp_back,t12_back]): # Plot all curves
            ax.plot([t/tau for t in t_go],vec_go,c=color,lw=2,label=labelm)
            ax.plot([t/tau for t in t_back],vec_back,c=color,lw=2)

        # Options for nice plotting
        for ax in [ax_t1,ax_t2,ax_dp,ax_t12]:
            ax.set_xlim(0,1)
            ax.set_xlabel("$t/\\tau$")
            ax.set_xticks(numpy.linspace(0,1,5))

        for ax in [ax_t1,ax_t2,ax_t12]:
            ax.set_ylim(0,numpy.pi)
            ax.set_yticks(numpy.linspace(0,numpy.pi,5))
            ax.set_yticklabels(["$0$","$\\pi/4$","$\\pi/2$","$3\\pi/4$","$\\pi$"])
        ax_dp.set_ylim(-numpy.pi,numpy.pi)
        ax_dp.set_yticks(numpy.linspace(-numpy.pi,numpy.pi,5))
        ax_dp.set_yticklabels(["$-\\pi$","$-\\pi/2$","$0$","$\\pi/2$","$\\pi$"])
        ax_t1.set_ylabel("$\\theta_1$")
        ax_t2.set_ylabel("$\\theta_2$")
        ax_t12.set_ylabel("$\\theta_{12}$")
        ax_dp.set_ylabel("$\\Delta\\Phi$")
        ax_dp.legend(loc='upper right') # Fill the legend with the precessional morphology

    fig.savefig("spin_angles.pdf",bbox_inches='tight') # Save pdf file





def phase_resampling():
    '''
    Precessional phase resampling. The magnidute of the total spin S is sampled
    according to |dS/dt|^-1, which correspond to a flat distribution in t(S).
    Output is saved in ./phase_resampling.pdf and data stored in
    `precession.storedir'/phase_resampling_.dat


    **Run using**

        import precession.test
        precession.test.phase_resampling()
    '''

    fig=pylab.figure(figsize=(6,6)) #Create figure object and axes
    ax_tS=fig.add_axes([0,0,0.6,0.6]) #bottom-left
    ax_td=fig.add_axes([0.65,0,0.3,0.6]) #bottom-right
    ax_Sd=fig.add_axes([0,0.65,0.6,0.3]) #top-left

    q=0.5   # Mass ratio. Must be q<=1.
    chi1=0.3 # Primary spin. Must be chi1<=1
    chi2=0.9 # Secondary spin. Must be chi2<=1
    M,m1,m2,S1,S2=precession.get_fixed(q,chi1,chi2) # Total-mass units M=1
    r=200.*M # Separation. Must be r>10M for PN to be valid
    J=3.14 # Magnitude of J: Jmin<J<Jmax as given by J_lim
    xi=-0.01 # Effective spin: xi_low<xi<xi_up as given by xi_allowed
    Sb_min,Sb_max=precession.Sb_limits(xi,J,q,S1,S2,r) # Limits in S
    tau=precession.precession_period(xi,J,q,S1,S2,r) # Precessional period
    d=2000 # Size of the statistical sample

    os.system("mkdir -p "+precession.storedir) # Create store directory, if necessary
    filename=precession.storedir+"/phase_resampling.dat" # Output file name
    if not os.path.isfile(filename): # Compute and store data if not present
        out=open(filename,"w")
        out.write("# q chi1 chi2 r J xi d\n") # Write header
        out.write( "# "+' '.join([str(x) for x in (q,chi1,chi2,r,J,xi,d)])+"\n")

        # S and t values for the S(t) plot
        S_vals=numpy.linspace(Sb_min,Sb_max,d)
        t_vals=numpy.array([abs(precession.t_of_S(Sb_min,S,Sb_min,Sb_max,xi,J,q,S1,S2,r)) for S in S_vals])
        # Sample values of S from |dt/dS|. Distribution should be flat in t.
        S_sample=numpy.array([precession.samplingS(xi,J,q,S1,S2,r) for i in range(d)])
        t_sample=numpy.array([abs(precession.t_of_S(Sb_min,S,Sb_min,Sb_max,xi,J,q,S1,S2,r)) for S in S_sample])
        # Continous distributions (normalized)
        S_distr=numpy.array([2.*abs(precession.dtdS(S,xi,J,q,S1,S2,r)/tau) for S in S_vals])
        t_distr=numpy.array([2./tau for t in t_vals])

        out.write("# S_vals t_vals S_sample t_sample S_distr t_distr\n")
        for Sv,tv,Ss,ts,Sd,td in zip(S_vals,t_vals,S_sample,t_sample,S_distr,t_distr):
            out.write(' '.join([str(x) for x in (Sv,tv,Ss,ts,Sd,td)])+"\n")
        out.close()
    else:  # Read
        S_vals,t_vals,S_sample,t_sample,S_distr,t_distr=numpy.loadtxt(filename,unpack=True)

    # Rescale all time values by 10^-6, for nicer plotting
    tau*=1e-6; t_vals*=1e-6; t_sample*=1e-6; t_distr/=1e-6

    ax_tS.plot(S_vals,t_vals,c='blue',lw=2)  # S(t) curve
    ax_td.plot(t_distr,t_vals,lw=2.,c='red') # Continous distribution P(t)
    ax_Sd.plot(S_vals,S_distr,lw=2.,c='red') # Continous distribution P(S)
    ax_td.hist(t_sample,bins=60,range=(0,tau/2.),normed=True,histtype='stepfilled', color="blue",alpha=0.4,orientation="horizontal") # Histogram P(t)
    ax_Sd.hist(S_sample,bins=60,range=(Sb_min,Sb_max),normed=True,histtype='stepfilled', color="blue",alpha=0.4) # Histogram P(S)

    # Options for nice plotting
    ax_tS.set_xlim(Sb_min,Sb_max)
    ax_tS.set_ylim(0,tau/2.)
    ax_tS.set_xlabel("$S/M^2$")
    ax_tS.set_ylabel("$t/(10^6 M)$")
    ax_td.set_xlim(0,0.5)  
    ax_td.set_ylim(0,tau/2.)
    ax_td.set_xlabel("$P(t)$")
    ax_td.set_yticklabels([])
    ax_Sd.set_xlim(Sb_min,Sb_max)
    ax_Sd.set_ylim(0,20)  
    ax_Sd.set_xticklabels([])
    ax_Sd.set_ylabel("$P(S)$")

    fig.savefig("phase_resampling.pdf",bbox_inches='tight') # Save pdf file


def PNwrappers():
        
    q=0.9  # Mass ratio. Must be q<=1.
    chi1=0.5 # Primary spin. Must be chi1<=1
    chi2=0.5 # Secondary spin. Must be chi2<=1
    M,m1,m2,S1,S2=precession.get_fixed(q,chi1,chi2) # Total-mass units M=1
    ri=1000*M  # Initial separation.
    rf=10.*M   # Final separation.
    rt=100.*M  # Intermediate separation for hybrid evolution.
    r_vals=numpy.logspace(numpy.log10(ri),numpy.log10(rf),1000) # Output requested

    t1i=numpy.pi/4.; t2i=numpy.pi/4.; dpi=numpy.pi/4. # Initial configuration
    xii,Ji,Si=precession.from_the_angles(t1i,t2i,dpi,q,S1,S2,ri)
    print "Configuration at r=ri"
    print "\t (xi,J,S)=(%.3f,%.3f,%.3f)" %(xii,Ji,Si)
    print "\t (theta1,theta2,deltaphi)=(%.3f,%.3f,%.3f)" %(t1i,t2i,dpi)

    print "\n *Orbit-averaged evolution*"
    print "Evolution ri --> rf"
    Jf,xif,Sf=precession.orbit_averaged(Ji,xii,Si,r_vals,q,S1,S2)
    print "\t (xi,J,S)=(%.3f,%.3f,%.3f)" %(xif[-1],Jf[-1],Sf[-1])
    t1f,t2f,dpf=precession.orbit_angles(t1i,t2i,dpi,r_vals,q,S1,S2)
    print "\t (theta1,theta2,deltaphi)=(%.3f,%.3f,%.3f)" %(t1f[-1],t2f[-1],dpf[-1])
    Lx,Ly,Lz,S1x,S1y,S1z,S2x,S2y,S2z=precession.orbit_vectors(Ji,xii,Si,r_vals,q,S1,S2)
    print "\t (Lx,Ly,Lz)=(%.3f,%.3f,%.3f)" %(Lx[-1],Ly[-1],Lz[-1])
    print "\t (S1x,S1y,S1z)=(%.3f,%.3f,%.3f)" %(S1x[-1],S1y[-1],S1z[-1])
    print "\t (S2x,S2y,S2z)=(%.3f,%.3f,%.3f)" %(S2x[-1],S2y[-1],S2z[-1])

    print "\n *Orbit-averaged evolution*"  
    print "Evolution ri --> rf"
    Jf=precession.evolve_J(xii,Ji,r_vals,q,S1,S2)
    print "\t (xi,J,S)=(%.3f,%.3f,-)" %(xii,Jf[-1])
    t1f,t2f,dpf=precession.evolve_angles(t1i,t2i,dpi,r_vals,q,S1,S2)
    print "\t (theta1,theta2,deltaphi)=(%.3f,%.3f,%.3f)" %(t1f[-1],t2f[-1],dpf[-1])
    print "Evolution ri --> infinity"
    kappainf=precession.evolve_J_backwards(xii,Jf[-1],rf,q,S1,S2)
    print "\t kappainf=%.3f" %kappainf    
    Jf=precession.evolve_J_infinity(xii,kappainf,r_vals,q,S1,S2)
    print "Evolution infinity --> rf"
    print "\t J=%.3f" %Jf[-1] 

    print "\n *Hybrid evolution*"  
    print "Prec.Av. infinity --> rt & Orb.Av. rt --> rf"
    t1f,t2f,dpf=precession.hybrid(xii,kappainf,r_vals,q,S1,S2,rt)
    print "\t (theta1,theta2,deltaphi)=(%.3f,%.3f,%.3f)" %(t1f[-1],t2f[-1],dpf[-1])
    



#parameter_selection()
#spin_angles()
#phase_resampling()
#PNevolve()



#phase_resampling()
#spin_angles()
#parameter_selection()