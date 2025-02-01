$7^{\text {th }}$ International Conference on Fatigue Design, Fatigue Design 2017, 29-30 November 2017, Senlis, France

# Experimental study of weld fatigue strength reduction for a stainless steel piping component 

Dave Hannes ${ }^{a *}$, Thomas Svensson ${ }^{b}$, Andreas Anderson ${ }^{c}$, Magnus Dahlberg ${ }^{a}$<br>${ }^{a}$ Kiwa Inspecta Technology, Lindhagensterrassen 1, 10425 Stockholm, Sweden<br>${ }^{b}$ TS IngenjÃ¶rsstatistik, BoviksvÃ¤gen 21, 50493 BorÃ¥s, Sweden<br>${ }^{c}$ RISE Research Institutes of Sweden, 50115 BorÃ¥s, Sweden


#### Abstract

An experimental mean curve and a design fatigue curve corresponding to $95 \%$ survival probability were derived from realistic fatigue experiments on a non-welded water pressurized piping component with primarily focus on high cycle fatigue. The components were subjected to a synthetic variable amplitude bending deformation. Comparison with the results obtained for a similar piping component with a circumferential butt weld allowed the determination of an experimental fatigue strength reduction factor. Comparison with the fatigue procedure and design curve in ASME BPVC Section III allowed to quantify its conservatism with regards to accounting for the presence of a weldment and more generally transferability.


(C) 2018 The Authors. Published by Elsevier Ltd.

Peer-review under responsibility of the scientific committee of the 7th International Conference on Fatigue Design.
Keywords: austenitic stainless steel; welded pipe; experimental strain analysis; spectrum loading; high cycle fatigue.

## 1. Introduction

Weldments are considered critical for the fatigue strength of structures or components. Fatigue cracks do namely tend to occur in the vicinity of welding joints rather than in the smooth base material. Welds represent indeed a local structural discontinuity or stress concentration which results in a general fatigue strength reduction, i.e. the load level

[^0]
## Nomenclature

A factor in Langer fatigue model
$B \quad$ exponent in Langer fatigue model
C cut-off limit in Langer fatigue model
$i \quad$ dummy index
$k \quad$ scaling factor
$K_{\mathrm{f}} \quad$ fatigue strength reduction factor
$K_{\mathrm{t}} \quad$ notch or concentration factor
$n \quad$ number of cycles in a load spectrum with strain amplitudes exceeding the cut-off limit
$N \quad$ number of cycles or predicted fatigue life
$q \quad$ notch sensitivity factor
$\varepsilon_{\mathrm{a}} \quad$ axial strain amplitude
$\|\bullet\|_{B C} \quad B C$-norm or equivalent measure
inducing a given fatigue life will typically be lower for the component or structure including a welding joint. The stress concentration introduced by the weld can be related to geometrical notches in for instance weld toes or different local material properties resulting from the welding process. In design, the fatigue strength reduction factor (FSRF), here denoted $K_{\mathrm{f}}$, quantifies this detrimental effect of a stress concentration. This quantity is also designated as the fatigue notch factor or fatigue effective stress concentration factor. In the case of a welding joint, it is defined for a given number of cycles as the ratio of the fatigue strengths of the smooth or plain component and the welded component. It is often approximated conservatively by the stress concentration or notch factor denoted $K_{\mathrm{t}}$. Different formula relating both factors have been proposed in the literature [1], but a classic approach introduces the notch sensitivity factor [2], $q$, defined in Eq. (1):

$$
q=\frac{K_{f}-1}{K_{t}-1}
$$

It varies in the range 0 to 1 . For $q$ approaching 0 , the material is considered notch insensitive as microstructural plastic deformation effectively relieves the stress concentration. Consequently the presence of a notch or discontinuity does then hardly affect the components fatigue strength. However for $q=1$, a limited amount of microstructural plastic deformation does not reduce the stress concentration yielding $K_{\mathrm{f}}=K_{\mathrm{t}}$. Accurate measures of the FSRF for a given weld are however best determined experimentally, due to the significant number of parameters affecting its value.

ASME Boiler and Pressure Vessel Code Section III [3] covers design and construction rules for nuclear facility components. For design against fatigue, the code includes material specific design curves (WÃ¶hler diagrams) and accounts for the reduction in fatigue strength of welded components using FSRFs [4]. Lifetime extension of nuclear power plants requires amongst others revised assessments of components to determine remaining fatigue life. Good understanding and increased knowledge about the inherent conservatism in the ASME III code is therefore crucial to avoid unnecessary over-conservatism, which may result in costly inspection programs or replacements.

The ASME fatigue design curve is constructed from a mean curve using adjustments factors [5]. These factors are supposed to account for the fundamental issue of transferability. The design curve is namely intended to be applicable for realistic components subjected to realistic loading conditions, whereas the original mean curve is generally obtained from experimental data for small, smooth test specimens subjected to constant amplitude loading. In an earlier investigation, the margins of the fatigue design curve for austenitic stainless steel in ASME III were investigated for a realistic piping component with a circumferential butt weld, see [6]. A water pressurized welded piping component with nominal wall thickness of 3 mm was subjected to variable amplitude, reversed bending deformation, see experimental set-up in Fig. 1(a). The welding joint was in as-welded condition, see Fig. 1(b). The weld capping was not removed which induced geometrical irregularities. This previous investigation highlighted
extensive conservatism in the ASME approach to transferability, but the magnitude of the margins depended largely on the FSRF related to
![](https://copilot-test.s3.amazonaws.com/uploaded/test_6/figures/2024_11_27_398ab78b16510fddec17g-3_139_321_1585_880.jpeg)

Fig. 1. (a) Experimental set-up with custom-build fixtures; (b) Piping component with circumferential butt weld in as-welded condition; (c) Smooth, non-welded piping component with central circumferential notch to localize fatigue initiation with (d) a sketch of its cross-section.
the considered weld. The current study aims therefore at a more accurate estimation of the FSRF through an experimental study. Fatigue tests on a similar plain or non-welded piping component, see Figs. 1(c) and (d), are performed.

## 2. Specimens

The plain test specimens were manufactured from straight, seamless TP 304 L stainless steel hot finished pipes (Sandvik 3R12). The austenitic material is consistent with the one used for the welded piping component in [6], but the manufacturing processes differ. The welded piping components were namely cold worked, which affects the ductility of the material. This discrepancy was however assumed to have a minor effect on the materials fatigue strength.

The nominal geometry of the original piping was identical to the one used in [6], i.e. with an outer diameter of 60.33 mm and a wall thickness equal to 5.54 mm . In the central part of the specimen the nominal wall thickness was reduced to 4 mm with shoulders in the transition region to avoid issues related to contact fatigue in the vicinity of the clamping region. To reduce the material volume subjected to significant fatigue loads and localize fatigue failure, a large circumferential notch was machined in the center of the specimen. The notch radius was 75 mm and the nominal wall thickness at the center of the notch was 3 mm . The latter is consistent with the nominal wall thickness of the welded piping component and crucial to consistent comparison with a leakage based failure criterion. The geometry of the machined plain test specimens, prior to welding of the lids at its extremities, is illustrated in Figs. 1(c) and (d).

Ideally the non-welded piping geometry should be un-notched, as the notch will inevitably somewhat reduce the fatigue strength of the considered plain piping component. However austenitic stainless steels exhibit relatively low notch sensitivity [7], with handbook recommendations [8] suggesting a notch sensitivity factor in the range 0.2 - 0.4
for annealed austenitic stainless steel. As a result the fatigue strength of the considered notched piping component was considered a good approximation of the fatigue strength for the un-notched piping component with nominal wall thickness 3 mm .

## 3. Experimental equipment and loading

To maintain consistency with the previous work performed on the welded piping component, an identical experimental set-up was used for the fatigue test in the current study, see Fig. 1(a). The specimens were subjected to reversed bending deformation with prescribed displacement control. The experimental set-up introduces further a minor cyclic membrane stress. The moment arm was 300 mm and the distance between the fixtures was about 205 mm . The piping component was water pressurized at 70 bar , reflecting realistic loading conditions for nuclear piping and introducing a minor tensile static load, as discussed in [6]. Testing was performed at room temperature and the local axial strains in the bending plane in the notch were recorded continuously with 2 strain gages with gage length 2 mm , see Fig. 1(d).

Leakage was detected by the pressure actuator displacement increase exceeding a pre-set level. It constitutes a realistic failure criterion for the fatigue tests. The specimens were subjected to variable amplitude loading applied in load blocks of approximately 43.2 s containing 453 load cycles, see Fig. 2. The signal was scaled to allow fatigue testing at different severities or strain amplitudes. The spectrum is a synthetic Gaussian spectrum similar to the variable amplitude loading used in the analysis of the welded piping component in [6]. A run-out limit set at 11000 load blocks was defined.
![](https://copilot-test.s3.amazonaws.com/uploaded/test_6/figures/2024_11_27_398ab78b16510fddec17g-4_298_1082_1258_510.jpeg)

Fig. 2. Illustration of a load block of the synthetic Gaussian spectrum constituting the variable amplitude loading applied during fatigue testing.

## 4. Theory and methods

Theoretical considerations and applied methods used for the analysis and assessment of the experimental results are mainly identical with those used in the previous work on the welded piping component, see [6] for more details.

### 4.1. Fatigue model

Different fatigue models exist which relate fatigue life or number of cycles, $N$, to a load parameter. In the current investigation the axial strain amplitude was used to define the load level, which allows direct comparison with the ASME fatigue design curve. In order to preserve consistency with ASME, the Langer fatigue model [9] was used to perform the analyses. The mean curve used in the construction of the studied ASME design curve is namely the Langer fatigue model [5]. This fatigue model is expressed in terms of three model parameters, $A, B$ and $C$, representing respectively a factor or constant, an exponent or slope and a cut-off limit or asymptote. The logarithmic form of the model reads,

$$
\ln N=\ln A-B \ln \left(\left\|\varepsilon_{a}\right\|_{B C}-C\right)
$$

where $\left\|\varepsilon_{a}\right\|_{B C}$ is an equivalent strain measure. The use of an equivalent strain measure is a generalization from the more common formulation with a constant strain amplitude, but here required for variable amplitude loading. The selected equivalent strain measure is the $B C$-norm, see Eq. (3), which yields the same accumulated damage as the full spectrum based on the Palmgren-Miner's linear damage rule [10,11].

$$
\left\|\varepsilon_{a}\right\|_{B C}=\left(\frac{1}{n} \sum_{i}^{n}\left(\varepsilon_{a, i}-C\right)^{B}\right)^{1 / B}+C
$$

The sum in Eq. (3) only considers the $n$ cycles included in the considered load sequence with strain amplitudes exceeding the cut-off limit $C$, as only these load cycles are assumed to contribute to fatigue damage accumulation. The Langer model reduces to the classic Basquin model [12], for $C=0$.

The model parameters are determined with the maximum-likelihood methodology. The logarithmic life is then assumed to follow a normal distribution. Besides the three model parameters, this probabilistic approach also yields an estimate of the standard deviation of the random error in logarithmic fatigue life. This estimate equals then approximately the coefficient of variation of the fatigue life. More details on the applied fitting procedure can be found in [13].

### 4.2. FSRF determination

The current investigation includes fatigue tests on smooth, plain piping components. Comparison with the results for a similar welded piping component investigated in previous work [6], allows an experimental estimate of the FSRF for the previously studied circumferential butt weld. The numerical procedure used in the estimation of a constant $K_{\mathrm{f}}$ is based on the maximum-likelihood methodology. The data sets from the welded and non-welded pipes are then considered simultaneously. The model used in the likelihood estimation is similar to Eq. (2), but includes an additional scaling factor $k$, see Eq. (4), directly applied to the strain amplitudes included in the load spectra recorded for each specimen.

$$
\ln N=\ln A-B \ln \left(\left\|k \varepsilon_{a}\right\|_{B C}-C\right)
$$

The scaling factor is $k=1$ for the non-welded specimens, and a positive constant when applied to the nominal strain amplitudes for the welded pipes. The optimal value of $k$ is then considered to be an estimate of $K_{\mathrm{f}}$. In the numerical procedure, the cut-off limit $C$ is kept constant and chosen to be equal to the estimate from the parameter estimation for the plain pipes. A sensitivity study showed that this somewhat arbitrary choice did not influence the estimated $K_{\mathrm{f}}$ significantly.

### 4.3. ASME margins

The numerical procedure for the parameter estimation in the fatigue model detailed in Eq. (2), yields as mentioned an estimate of the standard deviation of the logarithmic life. This estimate is consequently used to determine an approximate $90 \%$ lower prediction limit. This limit represents then a $95 \%$ survival probability and can be used as a component specific design curve. The empirical approach behind the derivation of component specific design curves was also used in [6]. The design curves are thus obtained through a specific horizontal shift leftwards of the fitted mean curve in a WÃ¶hler diagram.

A consistent comparison and study of the fatigue design curve for austenitic stainless steel in ASME III [3] is performed by means of the empirical design curves derived for the investigated piping components and corresponding to $95 \%$ survival probability. For the non-welded pipes the comparison can be performed directly with
the tabulated ASME design curve, whereas a reduction (vertical shift, downwards) of the ASME design curve is required for the welded pipes. The empirical design curve for the welded pipes was indeed derived based on a nominal strain measure. The reduction factor used in the current investigation is the experimentally determined estimate of the FSRF.

## 5. Results and discussion

From a total of 19 fatigue tests, 13 experiments were considered valid including one run-out [14]. For these thirteen experiments the recorded maximum strain amplitude was approximately in the range $0.2-0.4 \%$. However the remaining load cycles in a load block yielded significantly lower strain amplitudes, which will result in lower equivalent strain measures. The valid data points have been used in the derivation of a mean fatigue curve for the non-welded piping component and the experimental estimate of $K_{\mathrm{f}}$.

### 5.1. Mean curves

The obtained fitting parameters for the Langer fatigue model are presented in Tab. 1 and illustrated in Fig. (3). The different estimates depend on the considered data set. The results obtained for the welded piping component are reproduced from [6]. The number of cycles in the Langer model only considers the load cycles contributing to fatigue damage accumulation. Hence, the number of cycles related to the experimental data points shown in Fig. (3) differs from the total number of cycles actually applied to the considered test specimen during testing, as variable loading was used. For the non-welded pipes in the current investigation, the number of cycles contributing to damage represented between 25 and $50 \%$ of the total number of cycles.

The model parameters for different data sets in Tab. 1 do not show large discrepancies, except for parameter $A$, which is related to a shift in the WÃ¶hler diagram. The estimates of $A$ obtained in the current study are significantly larger than the one obtained in [6] for the welded piping component. This is explained by and consistent with a fatigue strength reduction due to the welding joint. The cut-off limit $C$ is a specificity of the Langer model. For the plain specimens the $95 \%$ confidence interval of $C$ was estimated. It was found to be relatively wide and includes zero. Hence, with this uncertainty related to the estimate of $C$, it could not be considered significantly different from zero. Consequently, the Langer model would then reduce to the classic Basquin model. Additional investigations using the Basquin model are presented in [14].

Table 1. Langer fatigue model parameters considering different data sets.

| Considered data sets | Welded from [6] | Non-welded | Welded and non-welded |
| :--- | :--- | :--- | :--- |
| Number of data points | 13 | 13 | 26 |
| Estimate of factor $A$ | 128 | 591 | 416 |
| Estimate of exponent $B$ | 2.01 | 2.07 | 2.22 |
| Estimate of cut-off limit $C$ | $0.058 \%$ | $0.056 \%$ | $0.056 \%(*)_{*} \%$ |

(*) kept fixed during estimation of remaining parameters and the estimate of the FSRF.
![](https://copilot-test.s3.amazonaws.com/uploaded/test_6/figures/2024_11_27_398ab78b16510fddec17g-7_283_249_1288_515.jpeg)

Fig. 3. WÃ¶hler diagrams for the different fitted Langer fatigue models. The experimental data points are plotted with $B=2.22, C=0.056 \%$ and for the welded data with a scaling factor equal to $K_{\mathrm{f}}=1.79$. The cut-off limit $C$ or asymptote is represented by the red dotted horizontal.

### 5.2. FSRF

The fitting to the non-welded and scaled welded data, see Tab 1 and Fig. 3, yielded an estimate of $K_{\mathrm{f}}=1.79 \pm$ 0.13 . The experimental estimate of the FSRF is significantly lower than the value of 3.24 following the recommendations of ASME [3,6]. The FSRF recommended by ASME includes thus a significant amount of conservatism for the considered welding joint.

The results in Fig. 3 do not show a clear dependency of the FSRF on the load level or number of cycles. A more detailed investigation using the Basquin model confirmed no significant difference in slope when considering the different datasets separately, see [14]. Hence the results support the assumption of a constant FSRF used in the numerical procedure. The experimental study has high cycle fatigue as main focus and does not cover low cycle fatigue, which may explain that a reduction in FSRF for high load levels, as reported in [4], is not observed.

Using the experimental estimate of the FSRF and Eq. (1), one can estimate the average concentration factor for the considered circumferential butt weld in as-welded condition. For a notch sensitivity factor of $0.3, K_{\mathrm{t}}$ equals then approximately 3.63 . Such a low notch sensitivity factor is only estimated relevant for annealed austenitic stainless steel piping. The welded piping in [6] was not annealed, but cold worked during manufacturing, which increases the notch sensitivity [8]. As a result the average notch factor related to the investigated welded piping in [6] is expected to be considerably less than 3.

### 5.3. Design curves

The fitting procedure for the welded and non-welded datasets yielded both a standard deviation of the logarithmic fatigue life equal to 0.36 . The resulting experimentally derived design curves corresponding to $95 \%$ survival probability are illustrated with dashed lines in Fig. 4. The empirical procedure is based on a horizontal shift of the mean curve. Hence the component specific design curves based on the Langer fatigue model share the asymptote for large number of cycles with the mean curve. An additional horizontal shift of the empirical design curve in this region is thus recommended and could be based on an estimate of the variation of the fatigue limit.

The reduced ASME design curve is to be used in conjunction with an equivalent strain measure based on nominal strain amplitudes. Comparison of the empirical design curves with the ASME design curve for the non-welded component and the reduced ASME design curve for the welded piping allows quantification of the margins in the ASME approach to transferability. The reduction factor in allowable fatigue life (horizontal translation) using the ASME design curve for the non-welded and welded components is respectively at least 1.6 and 2.3. Considerable conservatism in the ASME approach to transferability is thus highlighted, which supports the findings in [5].
![](https://copilot-test.s3.amazonaws.com/uploaded/test_6/figures/2024_11_27_398ab78b16510fddec17g-8_270_251_1303_515.jpeg)

Fig. 4. WÃ¶hler diagrams with design curves corresponding to $95 \%$ survival probability based on ASMEs recommendations and experimental results for both the welded and non-welded piping components.

## 6. Conclusions

Fatigue tests on water pressurized non-welded austenitic stainless steel piping components were performed with realistic variable amplitude bending deformation. The results allowed to quantify the fatigue strength reduction related to the circumferential butt weld in as-welded condition studied in [6]. The findings of the performed investigation are listed below.

- The experimental estimate of the FSRF is approximately equal to 1.8 for the considered welded piping.
- The experimental results did not show any dependency of the FSRF on load level or number of cycles.
- The corresponding factor proposed by ASME is significantly larger, hence yielding considerable conservatism.
- The ASME design curve corresponds to a probability of survival in excess of $95 \%$ for the considered pipes.
- Extensive conservatism in the ASME approach to transferability is highlighted.
- For the welded piping component, comparison with component specific design curves shows a margin on allowable fatigue life of at least 2.3.

The work contributed to better understanding of the transferability issue for welded piping components subjected to realistic loading. Component specific design curves were derived and support the claim of extensive conservatism in ASMEs design curves. More fatigue testing on realistic components is recommended to formulate generalizations of the findings in the current study.

## Acknowledgements

The authors gratefully acknowledge the financial support from the Swedish Radiation Safety Authority, RISE Research Institutes of Sweden and Ringhals AB. The material for the test specimens was kindly provided by Sandvik AB.

## References

[1] Y. Weixing, X. Kaiquan and G. Yi, On the fatigue notch factor, Kf, Int. J. Fatigue, 17 (1995) 245-251.
[2] R.E. Peterson, Notch-sensitivity, In: Sines, Waisman, (editors) Metal fatigue, (1959) Chapter 13.
[3] ASME, Boiler and Pressure Vessel Code, Section III, Rules for Construction of Nuclear Facility Components, 2013.
[4] C.E. Jaske, Fatigue-Strength-Reduction Factors for Welds in Pressure Vessels and Piping, J. Pressure Vessel Tech., 122 (2000) 297-304.
[5] O. Chopra and W. Shack, Effect of LWR Coolant Environments on the fatigue Life of Reactor Materials, NUREG/CR-6909, 2007.
[6] M. Dahlberg, D. Hannes and T. Svensson, Evaluation of fatigue in austenitic stainless steel pipe components, SSM 2015:38, 2015.
[7] C. Yen and T. Dolan, A Critical Review of the Criteria for Notch-Sensitivity in Fatigue of Metals, Univ. of Illinois, Urbana Champaign, 1952.
[8] B. SundstÃ¶m, Handbook of Solid Mechanics, KTH Royal Institute of Technology, Stockholm, 2010.
[9] B. Langer, Design of Pressure Vessels for Low-Cycle Fatigue, ASME J. Basic Eng., 84 (1962) 389-402.
[10] A. Palmgren, Die Lebensdauer von Kullagern, VDI, (1925) 339-341.
[11] M. Miner, Cumulative damage in fatigue, J. Appl. Mech., 12 (1945) 159-164.
[12] O. Basquin, The exponential law of endurance tests, Proc. ASTM, 10 (1910) 625-630.
[13] P. Johannesson, T. Svensson and J. de MarÃ©, Fatigue life prediction based on variable amplitude tests, Int. J. Fatigue, 27 (2005) 954-965.
[14] D. Hannes, T. Svensson, A. Anderson and M. Dahlberg, Evaluation of weld fatigue reduction in austenitic stainless steel pipe components, SSM 2017:25, 2017 (In Press).


[^0]:    * Corresponding author. Tel.: +46 706882891.

    E-mail address: dave.hannes@inspecta.com and dave.hannes@kiwa.com
