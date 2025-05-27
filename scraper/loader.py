import json
import re

# Sample input (abbreviated for illustration — assume the full text is already here)
raw_text = """A-Lot Staff Parking	140 Pleasant Grove Rd, Ithaca, NY 14850	42.4584, -76.4767
A. D. White Gardens	121 Presidents Dr, Ithaca, NY 14850	42.4478, -76.4819
A. D. White House	121 Presidents Dr, Ithaca, NY 14850	42.4483, -76.4820
AAP Downtown Facility	531 Esty St., Ithaca, NY 14850	42.4430, -76.5102
AAP New York City Center	26 Broadway, New York, NY 10004	40.7387, -73.9946
Acacia	318 Highland Road, Ithaca, NY 14850	42.4587, -76.4873
Academic Surge Facility A	222 Tower Rd, Ithaca, NY 14850	42.4483, -76.4783
Academic Surge Facility B	220 Tower Rd, Ithaca, NY 14850	42.4481, -76.4783
Africana Studies and Research Center	310 Triphammer Rd, Ithaca, NY 14850	42.4574, -76.4823
Agriculture Waste Management Laboratory	236 Gallus Rd, Ithaca, NY 14850	42.4443, -76.4523
Alpha Chi Omega	210 Thurston Ave., Ithaca, NY 14850	42.4540, -76.4897
Alpha Delta Phi	777 Stewart Avenue, Ithaca, NY 14850	42.4508, -76.4898
Alpha Epsilon Phi	435 Wyckoff Ave Ithaca, NY 14850	42.4566, -76.4854
Alpha Epsilon Pi	140 Thurston Ave., Ithaca, NY 14850	42.4542, -76.4883
Alpha Gamma Rho	203 Highland Ave., Ithaca, NY 14850	42.4557, -76.4852
Alpha Phi	411 Thurston Ave., Ithaca, NY 14850	42.4533, -76.4839
Alpha Sigma Phi	804 Stewart Ave., Ithaca, NY 14850	42.4521, -76.4907
Alpha Xi Delta	40 Ridgewood, Ithaca, NY 14850	42.4554, -76.4897
Alpha Zeta	214 Thurston Ave., Ithaca, NY 14850	42.4541, -76.4872
Alumni Affairs and Development, Ithaca	130 E. Seneca St., Ithaca, NY 14850	42.4406, -76.4976
Alumni Affairs and Development, NYC	230 Park Avenue, New York, NY 10169	40.7458, -73.9821
Alumni House	626 Thurston Ave, Ithaca, NY 14850	42.4518, -76.4809
American Indian Program House	125 Triphammer Rd, Ithaca, NY 14850	42.4561, -76.4804
Anabel Taylor Hall	548 College Ave, Ithaca, NY 14850	42.4449, -76.4856
Animal Science Teaching and Research Barns	839 Campus Rd, Ithaca, NY 14850	42.4450, -76.4672
Anna Comstock House	520 Thurston Ave, Ithaca, NY 14850	42.4539, -76.4823
Appel Basketball Courts	259 Jessup Rd, Ithaca, NY 14850	42.4564, -76.4745
Aquaculture Building	121 Ecology Dr, Ithaca, NY 14850	42.4419, -76.4680
Arnot Teaching and Research Forest	611 County Route 13, Van Etten, NY 14889	42.2630, -76.6269
Arthropod Research Facility	226 Gallus Rd, Ithaca, NY 14850	42.4443, -76.4518
Atkinson Hall	350 Tower Rd, Ithaca, NY 14850	42.4480, -76.4732
B-Lot Staff Parking	957 Campus Rd, Ithaca, NY 14850	42.4463, -76.4635
B-Lot Visitor Parking	957 Campus Rd, Ithaca, NY 14850	42.4457, -76.4648
Bailey Hall	230 Garden Ave, Ithaca, NY 14850	42.4492, -76.4801
Baker Institute for Animal Health	Hungerford Hill Rd, Ithaca, NY 14850	42.4280, -76.4540
Baker Laboratory	259 East Ave, Ithaca, NY 14850	42.4502, -76.4818
Baker North	117 Gothics Way, Ithaca, NY 14850	42.4487, -76.4887
Baker South	123 Gothics Way, Ithaca, NY 14850	42.4485, -76.4884
Baker Tower	356 West Ave, Ithaca, NY 14850	42.4489, -76.4882
Balch Hall	600 Thurston Ave, Ithaca, NY 14850	42.4530, -76.4797
Barbara McClintock Hall	224 Cradit Farm Dr, Ithaca, NY 14850	42.4539, -76.4745
Bard Hall	126 Hollister Dr, Ithaca, NY 14850	42.4439, -76.4840
Barnes Hall	129 Ho Plz, Ithaca, NY 14850	42.4464, -76.4843
Bartels Hall	554 Campus Rd, Ithaca, NY 14850	42.4458, -76.4762
Barton Hall	117 Statler Dr, Ithaca, NY 14850	42.4460, -76.4807
Barton Hall (AgriTech)	15 Castle St, Geneva, NY 14456	42.8679, -76.9819
Barton Laboratory	630 W North St, Geneva, NY 14456	42.8753, -77.0057
Bauer Hall	148 Cradit Farm Dr, Ithaca, NY 14850	42.4536, -76.4785
Beebe Hall	110 Plantations Rd, Ithaca, NY 14850	42.4489, -76.4743
Belkin Squash Courts	230 Pine Tree Road, Ithaca, NY 14850	42.4350, -76.4656
Beta Theta Pi	100 Ridgewood Road, Ithaca, NY 14850	42.4559, -76.4899
Big Red Barn	135 Presidents Dr, Ithaca, NY 14850	42.4485, -76.4810
Bill and Melinda Gates Hall	107 Hoy Rd, Ithaca, NY 14853	42.4450, -76.4808
Biotechnology Building	526 Campus Rd, Ithaca, NY 14850	42.4464, -76.4784
Blair Farm Complex	705 Dryden Rd, Ithaca, NY 14850	42.4430, -76.4688
Blauvelt Laboratory	169 Helios Cir, Ithaca, NY 14850	42.4487, -76.4698
Boldt Hall	727 University Ave, Ithaca, NY 14850	42.4490, -76.4887
Boldt Tower	727 University Ave, Ithaca, NY 14850	42.4490, -76.4891
Botanic Gardens	124 Comstock Knoll Dr, Ithaca, NY 14850	42.4494, -76.4719
Botanic Gardens Parking	124 Comstock Knoll Dr, Ithaca, NY 14850	42.4493, -76.4718
Botanic Gardens Ramin Administrative Center	130 Forest Home Dr, Ithaca, NY 14850	42.4530, -76.4719
Bowers College of Computing and Information Science Building	127 Hoy Rd., Ithaca, NY 14850	42.4442, -76.4807
Boyce Thompson Institute	533 Tower Rd, Ithaca, NY 14850	42.4470, -76.4676
Bradfield Hall	306 Tower Rd, Ithaca, NY 14850	42.4479, -76.4758
Breazzano Family Center for Business Education	209-215 Dryden Road, Ithaca, Ithaca, NY 14850	42.4416, -76.4845
Bruckner Laboratory	208 Mann Dr, Ithaca, NY 14850	42.4483, -76.4741
Business and Technology Park	15 Thornwood Dr, Ithaca, NY 14850	42.4854, -76.4613
Buttermilk Falls State Park	112 E Buttermilk Falls Rd, Ithaca, NY 14850	42.4170, -76.5216
Caldwell Hall	121 Reservoir Ave, Ithaca, NY 14850	42.4492, -76.4783
Campus Warehouse (AgriTech)	81 Castle Creek Dr, Geneva, NY 14456	42.8750, -77.0094
Carl Becker House	647 Stewart Ave, Ithaca, NY 14850	42.4482, -76.4896
Carpenter Hall	313 Campus Rd, Ithaca, NY 14850	42.4448, -76.4842
Cascadilla Hall	115 Cascadilla Pl, Ithaca, NY 14850	42.4424, -76.4868
Cayuga Medical Center	101 Dates Dr, Ithaca, NY 14850	42.4692, -76.5375
Cayuga Nature Center	1420 Taughannock Blvd., Ithaca, NY 14850	42.5190, -76.5546
Center for Jewish Living	104 West Ave, Ithaca, NY 14850	42.4444, -76.4879
Central Heating Plant	651 Dryden Rd, Ithaca, NY 14850	42.4429, -76.4747
Charles H. Dyson School of Applied Economics and Management	137 Reservoir Ave, Ithaca, NY 14850	42.4492, -76.4771
Chesterton House	115 The Knoll, Ithaca, NY 14850	42.4537, -76.4901
Chi Phi	107 Edgemoor Lane, Ithaca, NY 14850	42.4437, -76.4888
Chi Psi	810 University Ave., Ithaca, NY 14850	42.4509, -76.4881
Chilled Water Plant	830 Campus Rd, Ithaca, NY 14850	42.4513, -76.4793
Clara Dickson Hall	21 Sisson Pl, Ithaca, NY 14850	42.4542, -76.4791
Clark Hall	142 Sciences Dr, Ithaca, NY 14850	42.4498, -76.4811
Collyer Boat House	685 Third St, Ithaca, NY 14850	42.4469, -76.5112
Companion Animal Hospital	930 Campus Rd, Ithaca, NY 14853	42.4469, -76.4646
Computing and Communications Center (CCC)	235 Garden Ave, Ithaca, NY 14850	42.4493, -76.4790
Comstock Hall	129 Garden Ave, Ithaca, NY 14580	42.4466, -76.4793
Convenient Care at Ithaca	10 Arrowwood Dr, Ithaca, NY 14850	42.4798, -76.4644
Cook House	709 University Ave, Ithaca, NY 14853	42.4488, -76.4896
Cornell AgriTech	630 W North St, Geneva, NY 14456	42.8771, -77.0077
Cornell Botanic Gardens Brian C. Nevin Welcome Center	124 Comstock Knoll Dr, Ithaca, NY 14850	42.4496, -76.4723
Cornell Child Care Center	150 Pleasant Grove Rd, Ithaca, NY 14850	42.4593, -76.4759
Cornell Club of New York City	6 E 44th St, New York, NY 10017	40.7544, -73.9793
Cornell Health	110 Ho Plz, Ithaca, NY 14853	42.4458, -76.4856
Cornell Orchards	709 Dryden Rd, Ithaca, NY 14850	42.4449, -76.4623
Corson Hall	215 Tower Rd, Ithaca, NY 14853	42.4473, -76.4783
Court Residence Hall	148 Cradit Farm Dr, Ithaca, NY 14850	42.4545, -76.4780
Dairy Bar	411 Tower Rd, Ithaca, NY 14853	42.4470, -76.4702
Dairy Barn (AgriTech)	69 Collier Dr, Geneva, NY 14456	42.8762, -77.0082
Day Hall	144 East Ave, Ithaca, NY 14850	42.4470, -76.4833
DeFrees Laboratory	527 College Ave, Ithaca, NY 14850	42.4447, -76.4848
Dean's Garden	124 Comstock Knoll Dr, Ithaca, NY 14850	42.4496, -76.4773
Delta Chi	102 The Knoll, Ithaca, NY 14850	42.4538, -76.4883
Delta Delta Delta	118 Triphammer Road, Ithaca, NY 14850	42.4554, -76.4814
Delta Gamma	117 Triphammer Rd., Ithaca, NY 14850	42.4555, -76.4805
Delta Kappa Epsilon	13 South Ave., Ithaca, NY 14850	42.4446, -76.4871
Delta Phi	100 Cornell Ave., Ithaca, NY 14850	42.4466, -76.4920
Delta Tau Delta	104 Mary Ann Wood Dr., Ithaca, NY 14850	42.4454, -76.4887
Delta Upsilon	6 South Ave., Ithaca, NY 14850	42.4451, -76.4872
Dilmun Hill Student Organic Farm	705 Dryden Rd, Ithaca, NY 14850	42.4432, -76.4692
Dimock Environmental Control Laboratory	129 Helios Cir, Ithaca, NY 14853	42.4485, -76.4683
Dolgen Hall	140 Garden Ave, Ithaca, NY 14850	42.4473, -76.4801
Downtown Ithaca	171 E M.L.K. Jr. St, Ithaca, NY 14850	42.4404, -76.4969
Duffield Hall	343 Campus Rd, Ithaca, NY 14850	42.4447, -76.4826
Dyce Laboratory	201 Freese Rd, Ithaca, NY 14850	42.4650, -76.4452
East Campus Research Facility	626 Tower Rd, Ithaca, NY 14850	42.4468, -76.4659
East Campus Service Center	209 Solidago Rd, Ithaca, NY 14850	42.4453, -76.4562
East Hill Office Building	395 Pine Tree Rd, Ithaca, NY 14850	42.4392, -76.4632
East Hill Plaza	315-335 Pine Tree Rd, Ithaca, NY 14850	42.4378, -76.4642
Ecology and Toxicology Fish Hatchery	145 Ecology Dr, Ithaca, NY 14850	42.4416, -76.4665
Eddy Gate	Cascadilla Pl, Ithaca, NY 14850	42.4424, -76.4875
Emerson Hall	236 Mann Dr, Ithaca, NY 14850	42.4484, -76.4758
Environmental Health & Safety	201 Palm Rd, Ithaca, NY 14850	42.4464, -76.4598
Equine Drug Sports Medicine Facility	913 Warren Dr, Ithaca, NY 14853	42.5005, -76.4665
Equine Metabolism Unit	833 Campus Rd, Ithaca, NY 14850	42.4445, -76.4675
Equine Park	Bluegrass Ln, Ithaca, NY 14850	42.4615, -76.4580
Equine and Farm Animal Hospitals	930 Campus Rd, Ithaca, NY 14853	42.4474, -76.4635
Facilities Services Recycling Center	251 Solidago Rd, Ithaca, NY 14850	42.4434, -76.4560
Faculty Tennis Club	168 Hoy Rd, Ithaca, NY 14850	42.4428, -76.4797
Fall Creek Studios	1201 North Tioga St, Ithaca, NY 14850	42.4534, -76.4976
Farm Service Shop	126 McGowan Woods Rd, Ithaca, NY 14850	42.4464, -76.4584
Federal Nutrition Lab	538 Tower Rd, Ithaca, NY 14850	42.4477, -76.4672
Fernow Hall	226 Mann Dr, Ithaca, NY 14850	42.4484, -76.4751
Fischell Band Center	141 Kite Hill Dr, Ithaca, NY 14850	42.4438, -76.4772
Flora Rose House	134 Gothics Way, Ithaca, NY 14850	42.4478, -76.4889
Floriculture Greenhouses	512 Tower Rd, Ithaca, NY 14850	42.4488, -76.4693
Food Research Lab (AgriTech)	665 West North St, Geneva, NY 14456	42.8774, -77.0093
Food Science Laboratory	423 Tower Rd, Ithaca, NY 14853	42.4471, -76.4704
Forest Home Dr. Parking Garage	37 Forest Home Dr, Ithaca, NY 14850	42.4509, -76.4790
Founders Hall	352 West Ave, Ithaca, NY 14850	42.4484, -76.4880
Foundry	936 University Ave, Ithaca, NY 14850	42.4515, -76.4835
Foundry Kiln Shed	936 University Ave, Ithaca, NY 14850	42.4516, -76.4837
Friedman Strength and Conditioning Center	554 Campus Rd, Ithaca, NY 14850	42.4455, -76.4758
Friedman Wrestling Center	610 Campus Rd, Ithaca, NY 14850	42.4456, -76.4745
Friends Hall	521 Campus Rd, Ithaca, NY 14850	42.4450, -76.4783
Fuertes Observatory	209 Cradit Farm Dr, Ithaca, NY 14850	42.4528, -76.4745
Ganedago: Hall	121 Triphammer Rd, Ithaca, NY 14850	42.4563, -76.4791
General Services Building (AgriTech)	33 Crabapple Dr, Geneva, NY 14456	42.8755, -77.0099
Goldwin Smith Hall	232 East Ave, Ithaca, NY 14850	42.4491, -76.4835
Graphic Arts Services Building	490 Pine Tree Rd, Ithaca, NY 14850	42.4434, -76.4712
Grossman Pond	124 Comstock Knoll Dr, Ithaca, NY 14850	42.4521, -76.4544
Grounds Operations Facility	275 Palm Rd, Ithaca, NY 14850	42.4459, -76.4573
Grumman Hall	134 Rhodes Dr, Ithaca, NY 14850	42.4434, -76.4821
Grumman Squash Courts	505 Campus Rd, Ithaca, NY 14850	42.4450, -76.4799
Guterman Bioclimatic Laboratory	105 Caldwell Rd, Ithaca, NY 14850	42.4475, -76.4605
Hanger Theatre	801 Taughannock Blvd, Ithaca, NY 14850	42.4551, -76.5172
Hans Bethe House	314 West Ave, Ithaca, NY 14850	42.4471, -76.4886
Harford Animal Science Teaching and Research Center	681 Cornell Ln, Harford, NY 13784	42.4415, -76.2482
Hartung-Boothroyd Observatory	553 Mount Pleasant Rd, Freeville, NY 13068	42.4582, -76.3846
Hasbrouck Apartments	121 Pleasant Grove Rd, Ithaca, NY 14850	42.4563, -76.4719
Hasbrouck Community Center	121 Pleasant Grove Rd, Ithaca, NY 14850	42.4563, -76.4719
Heating Plant (AgriTech)	152 Collier Dr, Geneva, NY 14456	42.8762, -77.0082
Hedrick Hall	630 W North St, Geneva, NY 14456	42.8768, -77.0074
Hedrick Hall (AgriTech)	635 West North St, Geneva, NY 14456	42.8772, -77.0078
Helen Newman Hall	163 Cradit Farm Dr, Ithaca, NY 14850	42.4530, -76.4774
High Voltage Laboratory	909 Mitchell St, Ithaca, NY 14850	42.4374, -76.4724
Ho Plaza	135 Ho Plz, Ithaca, NY 14850	42.4467, -76.4851
Hoffman Challenge Course Pavilion	466 Mount Pleasant Rd, Ithaca, NY 14850	42.4610, -76.3860
Holland International Living Center	128 Program House Dr, Ithaca, NY 14850	42.4556, -76.4761
Hollister Hall	527 College Ave, Ithaca, NY 14850	42.4440, -76.4845
Horticulture Greenhouse Range (AgriTech)	14 Castle Creek Dr, Geneva, NY 14456	42.8750, -77.0094
Horton Lab	512 Tower Rd, Ithaca, NY 14850	42.4487, -76.4688
Houston Pond	124 Comstock Knoll Dr, Ithaca, NY 14850	42.4511, -76.4546
Hoy Rd. Parking Garage	167 Hoy Rd, Ithaca, NY 14853	42.4440, -76.4796
Hu Shih Hall	141 Program House Dr, Ithaca, NY 14850	42.4553, -76.4749
Hughes Hall	241 Campus Rd, Ithaca, NY 14850	42.4437, -76.4863
Human Ecology Building	37 Forest Home Dr, Ithaca, NY 14850	42.4505, -76.4786
Humphreys Service Building	639 Dryden Rd, Ithaca, NY 14850	42.4427, -76.4755
Hurlburt House	111 Country Club Rd, Ithaca, NY 14850	42.4579, -76.4839
I Barn	231 Farrier Rd, Ithaca, NY 14850	42.4478, -76.4642
ILR Conference Center	140 Garden Ave, Ithaca, NY 14850	42.4470, -76.4801
ILR NYC Headquarters	570 Lexington Ave., New York City, NY 10022	40.7572, -73.9726
Imogene Powers Johnson Center for Birds and Biodiversity	159 Sapsucker Woods Rd, Ithaca, NY 14850	42.4799, -76.4511
Industrial & Labor Relations Research	140 Garden Ave, Ithaca, NY 14850	42.4466, -76.4801
Insectary Complex	169 Helios Cir, Ithaca, NY 14850	42.4489, -76.4699
Integrated Pest Management (IPM) (AgriTech)	607 West North St, Geneva, NY 14456	42.8770, -77.0066
Ithaca Bus Terminal	710 W. State St., Ithaca, NY 14850	42.4395, -76.5110
Ithaca Campus	144 East Ave, Ithaca, NY 14850	42.4470, -76.4800
Ithaca College	953 Danby Rd, Ithaca, NY 14850	42.4219, -76.4950
Ithaca Commons	171 E M.L.K. Jr. St, Ithaca, NY 14850	42.4396, -76.4968
Ithaca Farmers' Market	Steamboat Landing, 545 3rd St, Ithaca, NY 14851	42.4510, -76.5093
Ithaca High School	1401 N Cayuga St, Ithaca, NY 14850	42.4551, -76.4987
Ithaca Police Department	120 E Clinton St, Ithaca, NY 14851	42.4370, -76.4976
Ithaca Sciencenter	601 1st St, Ithaca, NY 14850	42.4498, -76.5045
Ithaca Tompkins Regional Airport	1 Culligan Dr, Ithaca, NY 14850	42.4898, -76.4623
Ives Hall	121 Tower Rd, Ithaca, NY 14850	42.4472, -76.4810
Ives Hall East	121 Tower Rd, Ithaca, NY 14850	42.4469, -76.4807
Ives Hall West	121 Tower Rd, Ithaca, NY 14850	42.4470, -76.4814
J Barn	231 Farrier Rd, Ithaca, NY 14850	42.4480, -76.4643
JAM (Just About Music)	142 Program House Dr, Ithaca, NY 14850	42.4551, -76.4761
James Law Auditorium	602 Tower Rd, Ithaca, NY 14853	42.4479, -76.4665
Jameson Hall	128 Northcross Rd, Ithaca, NY 14853	42.4557, -76.4782
Japes Lodge	139 Cradit Farm Dr, Ithaca, NY 14850	42.4524, -76.4798
Jennings Crabapple Collection	124 Comstock Knoll Dr, Ithaca, NY 14850	42.4530, -76.4538
Jessup Field	108 Jessup Rd, Ithaca, NY 14850	42.4572, -76.4806
Johnson Museum of Art	114 Central Ave, Ithaca, NY 14853	42.4507, -76.4861
Jordan Hall	630 W North St, Geneva, NY 14456	42.8774, -77.0072
Jordan Hall (AgriTech)	630 West North St, Geneva, NY 14456	42.8772, -77.0077
Judith Eisner Pavilion	430 College Ave, Ithaca, NY 14850	42.4427, -76.4854
K Barn	231 Farrier Rd, Ithaca, NY 14850	42.4481, -76.4644
Kahin Center	640 Stewart Ave, Ithaca, NY 14850	42.4480, -76.4913
Kappa Alpha Theta	519 Stewart Ave., Ithaca, NY 14850	42.4446, -76.4890
Kappa Delta	109 Triphammer Rd., Ithaca, NY 14850	42.4549, -76.4805
Kappa Delta Rho	312 Highland Road, Ithaca, NY 14850	42.4579, -76.4870
Kappa Kappa Gamma	508 Thurston Ave., Ithaca, NY 14850	42.4539, -76.4831
Kappa Sigma	600 University Ave,. Ithaca, NY 14850	42.4498, -76.4914
Kay Hall	148 Cradit Farm Dr, Ithaca, NY 14850	42.4541, -76.4780
Keeton House	4 Forest Park Ln, Ithaca, NY 14850	42.4467, -76.4895
Kennedy Hall	215 Garden Ave, Ithaca, NY 14850	42.4481, -76.4793
Kenneth Post Greenhouses	512 Tower Rd, Ithaca, NY 14850	42.4479, -76.4694
Kimball Hall	134 Hollister Dr, Ithaca, NY 14850	42.4439, -76.4832
King-Shaw Hall	140 Garden Ave, Ithaca, NY 14850	42.4469, -76.4801
Kinzelberg Hall	244 Garden Ave, Ithaca, NY 14850	42.4500, -76.4799
Klarman Hall	232 East Ave, Ithaca, NY 14850	42.4491, -76.4830
Kroch Library	216 East Ave, Ithaca, NY 14853	42.4480, -76.4835
L Barn	231 Farrier Rd, Ithaca, NY 14850	42.4482, -76.4645
Lambda Chi Alpha	125 Edgemoor Lane, Ithaca, NY 14850	42.4438, -76.4879
Langmuir Lab	95 Brown Rd, Ithaca, NY 14850	42.4856, -76.4586
Large Animal Research Teaching Unit	836 Campus Rd, Ithaca, NY 14850	42.4463, -76.4675
Leland Laboratory	121 Tuber Dr, Ithaca, NY 14850	42.4495, -76.4626
Liberty Hyde Bailey Conservatory	236 Tower Rd., Ithaca, NY 13835	42.4479, -76.4769
Library Annex-Storage Facility	209 Bookbank Rd, Ithaca, NY 14850	42.4425, -76.4580
Liddell Laboratory	118 Freese Rd, Ithaca, NY 14850	42.4606, -76.4443
Lincoln Hall	256 East Ave, Ithaca, NY 14850	42.4501, -76.4835
Little Moose Field Station	Outlet Rd, Old Forge, NY 13420	43.6811, -74.9407
Livestock Pavilion	48 Judd Falls Rd, Ithaca, NY 14850	42.4466, -76.4707
Louie's Lunch Truck	500 Thurston Ave, Ithaca, NY 14850	42.4534, -76.4813
Lynah Rink	536 Campus Rd, Ithaca, NY 14850	42.4457, -76.4774
Lyon Hall	336 West Ave, Ithaca, NY 14850	42.4478, -76.4880
M Barn	231 Farrier Rd, Ithaca, NY 14850	42.4484, -76.4645
Machine Shop	490 Pine Tree Rd, Ithaca, NY 14850	42.4432, -76.4712
Malott Hall	212 Garden Ave, Ithaca, NY 14850	42.4482, -76.4802
Mann Library	237 Mann Dr, Ithaca, NY 14853	42.4488, -76.4763
Maplewood Park	201 Maple Ave, Ithaca, NY 14850	42.4394, -76.4727
Maplewood Park Apartments Community Center	201 Maple Ave, Ithaca, NY 14850	42.4411, -76.4740
Martha Van Rensselaer East Building	116 Reservoir Ave, Ithaca, NY 14850	42.4501, -76.4780
Martha Van Rensselaer Hall	116 Reservoir Ave, Ithaca, NY 14850	42.4500, -76.4787
Martha Van Rensselaer West Building	116 Reservoir Ave, Ithaca, NY 14850	42.4502, -76.4791
Martin Y. Tang Welcome Center	616 Thurston Ave, Ithaca, NY 14850	42.4522, -76.4804
Mary Donlon Hall	115 Northcross Rd, Ithaca, NY 14850	42.4550, -76.4777
McFaddin Hall	324 West Ave, Ithaca, NY 14850	42.4472, -76.4880
McGovern Fields	126 Game Farm Rd, Ithaca, NY 14850	42.4390, -76.4508
McGraw Hall	141 Central Ave, Ithaca, NY 14850	42.4494, -76.4854
McGraw Tower	160 Ho Plaza, Ithaca, NY 14850	42.4476, -76.4851
Mennen Hall	342 West Ave, Ithaca, NY 14850	42.4480, -76.4881
Merrill Family Sailing Center	1000 E Shore Dr, Ithaca, NY 14850	42.4702, -76.5031
Mews Hall	172 Cradit Farm Dr, Ithaca, NY 14850	42.4544, -76.4769
Micro-Kelvin Laboratory	142 Sciences Dr, Ithaca, NY 14850	42.4492, -76.4812
Miller-Heller House	122 Eddy St, Ithaca, NY 14850	42.4390, -76.4876
Milstein Hall	943 University Ave, Ithaca, NY 14850	42.4512, -76.4836
Moakley House Golf Course	215 Warren Rd, Ithaca, NY 14850	42.4582, -76.4673
Moore Laboratory	602 Tower Rd, Ithaca, NY 14850	42.4480, -76.4657
Morrill Hall	159 Central Ave, Ithaca, NY 14850	42.4486, -76.4853
Morrison Hall	507 Tower Rd, Ithaca, NY 14850	42.4463, -76.4693
Mower Storage (AgriTech)	20 Innovation Blvd, Geneva, NY 14456	42.8574, -77.0349
Muenscher Laboratory	130 Tuber Dr, Ithaca, NY 14850	42.4497, -76.4632
Museum of the Earth	1259 Trumansburg Rd, Ithaca, NY 14850	42.4663, -76.5364
Myron Taylor Hall	524 College Ave, Ithaca, NY 14850	42.4440, -76.4856
Myron Taylor Jane Foster Library Addition	514 College Ave, Ithaca, NY 14850	42.4437, -76.4858
Nematode Lab	527 Tower Rd, Ithaca, NY 14850	42.4473, -76.4685
New York City		40.7059, -73.8959
New York State Veterinary Diagnostic Laboratory	240 Farrier Rd, Ithaca, NY 14850	42.4488, -76.4643
Newman Accelerator Building	153 Sciences Dr, Ithaca, NY 14850	42.4505, -76.4805
Newman Arboretum	124 Comstock Knoll Dr, Ithaca, NY 14850	42.4519, -76.4560
Newman Lab	153 Sciences Dr, Ithaca, NY 14850	42.4502, -76.4804
North Campus High Rise 5	225 Jessup Rd, Ithaca, NY 14850	42.4562, -76.4768
North Campus Low Rise 6	237 Jessup Rd, Ithaca, NY 14850	42.4563, -76.4761
North Campus Low Rise 7	116 Program House Dr, Ithaca, NY 14850	42.4562, -76.4754
North Campus Low Rise 9	142 Program House Dr, Ithaca, NY 14850	42.4549, -76.4761
North Campus Student Center	224 Jessup Rd, Ithaca, NY 14850	42.4573, -76.4769
North Campus Townhouse A	210 Jessup Rd, Ithaca, NY 14850	42.4570, -76.4779
North Campus Townhouse B	218 Jessup Rd, Ithaca, NY 14850	42.4571, -76.4773
North Campus Townhouse C	228 Jessup Rd, Ithaca, NY 14850	42.4570, -76.4767
North Campus Townhouse D	234 Jessup Rd, Ithaca, NY 14850	42.4572, -76.4763
North Campus Townhouse E	238 Jessup Rd, Ithaca, NY 14850	42.4570, -76.4760
North Campus Townhouse F	244 Jessup Rd, Ithaca, NY 14850	42.4572, -76.4757
North Campus Townhouse G	250 Jessup Rd, Ithaca, NY 14850	42.4570, -76.4753
North Campus Townhouse H	258 Jessup Rd, Ithaca, NY 14850	42.4573, -76.4749
Noyes Community and Recreation Center	306 West Ave, Ithaca, NY 14850	42.4465, -76.4880
Noyes Lodge	616 Thurston Ave, Ithaca, NY 14850	42.4522, -76.4801
Nursery Cellars (AgriTech)	5 Rootstock Dr, Geneva, NY 14456	42.8574, -77.0349
Oak Avenue	116 Oak Ave, Ithaca, NY 14850	42.4427, -76.4842
Olin Hall	113 Ho Plz, Ithaca, NY 14850	42.4454, -76.4844
Olin Library	161 Ho Plz, Ithaca, NY 14853	42.4479, -76.4842
Olive Tjaden Hall	909 University Ave, Ithaca, NY 14850	42.4509, -76.4854
Orchards Parking	709 Dryden Rd, Ithaca, NY 14850	42.4452, -76.4623
Oxley Equestrian Center	220 Pine Tree Rd, Ithaca, NY 14850	42.4340, -76.4646
Parking at Alumni House	626 Thurston Ave, Ithaca, NY 14850	42.4520, -76.4810
Parking at Art Museum	114 Central Ave, Ithaca, NY 14853	42.4510, -76.4860
Parking at Helen Newman	163 Cradit Farm Dr, Ithaca, NY 14850	42.4529, -76.4785
Parking at Toboggan Lodge	38 Forest Home Dr, Ithaca, NY 14850	42.4510, -76.4791
Parrot Hall	630 W North St, Geneva, NY 14456	42.8769, -77.0080
Peony Gardens		42.4491, -76.4725
Phi Delta Theta	2 Ridgewood Road, Ithaca, NY 14850	42.4548, -76.4895
Phi Gamma Delta	118 McGraw Place, Ithaca, NY 14850	42.4515, -76.4892
Phi Kappa Tau	106 The Knoll, Ithaca, NY 14850	42.4538, -76.4884
Phi Mu	509 Wyckoff Road, Ithaca, NY 14850	42.4572, -76.4871
Phi Sigma Sigma	14 South Ave., Ithaca, NY 14850	42.4450, -76.4878
Phillips Hall	116 Hoy Rd, Ithaca, NY 14850	42.4445, -76.4820
Physical Sciences Building	245 East Ave, Ithaca, NY 14850	42.4499, -76.4818
Pi Beta Phi	330 Triphammer Rd., Ithaca, NY 14850	42.4582, -76.4826
Pi Delta Psi	124 Triphammer Rd., Ithaca, NY 14850	42.4557, -76.4814
Pi Kappa Alpha	17 South Ave,. Ithaca, NY 14850	42.4445, -76.4884
Pi Kappa Phi	55 Ridgewood Rd, Ithaca, NY 14850	42.4555, -76.4885
Plant Breeding Love Laboratory	126 Medicago Dr, Ithaca, NY 14850	42.4492, -76.4620
Plant Pathology Greenhouse Complex	512 Tower Rd, Ithaca, NY 14850	42.4484, -76.4686
Plant Pathology Herbarium	214 Gallus Rd, Ithaca, NY 14850	42.4442, -76.4509
Plant Science Building	236 Tower Rd, Ithaca, NY 14850	42.4483, -76.4770
Plant Virology and Nematology Laboratory	129 Helios Cir, Ithaca, NY 14850	42.4480, -76.4683
Print Shop	490 Pine Tree Rd, Ithaca, NY 14850	42.4434, -76.4713
Prospect of Whitby	228 Wait Ave, Ithaca, NY 14850	42.4549, -76.4821
Prudence Risley Residential College	535 Thurston Ave, Ithaca, NY 14850	42.4531, -76.4819
Rand Hall	947 University Ave, Ithaca, NY 14850	42.4512, -76.4829
Raptor Facility	216 Raptor Rd, Ithaca, NY 14850	42.4425, -76.4508
Raw Products (AgriTech)	7 Crabapple Dr, Geneva, NY 14456	42.8755, -77.0099
Real Estate Department	15 Thornwood Dr., Ithaca, NY, 14850	42.4854, -76.4663
Reis Tennis Center	230 Pine Tree Rd, Ithaca, NY 14850	42.4350, -76.4654
Resource Ecology and Management Laboratory	139 Ecology Dr, Ithaca, NY 14850	42.4417, -76.4669
Rhodes Hall	136 Hoy Rd, Ithaca, NY 14853	42.4434, -76.4814
Rice Hall	340 Tower Rd, Ithaca, NY 14850	42.4479, -76.4741
Richard M. Lewis Education Center	130 Comstock Knoll Dr, Ithaca, NY 14853	42.4497, -76.4718
Riley-Robb Hall	111 Wing Dr, Ithaca, NY 14850	42.4458, -76.4712
Robert J & Helen Appel Commons	186 Cradit Farm Dr, Ithaca, NY 14850	42.4536, -76.4761
Robert Purcell Community Center	217 Jessup Rd, Ithaca, NY 14850	42.4559, -76.4775
Robert Trent Jones Golf Course	215 Warren Rd, Ithaca, NY 14850	42.4603, -76.4744
Robert W. Holley Center for Agriculture and Health	538 Tower Rd, Ithaca, NY 14850	42.4479, -76.4674
Roberts Hall	215 Garden Ave, Ithaca, NY 14850	42.4487, -76.4794
Robison Alumni Fields	240 Pine Tree Rd, Ithaca, NY 14850	42.4468, -76.4752
Robison Shellhouse	687 Third St, Ithaca, NY 14850	42.4467, -76.5113
Robison Softball Field	220 Pine Tree Road, Ithaca, NY 14850	42.4356, -76.4662
Rockefeller Hall	231 East Ave, Ithaca, NY 14850	42.4490, -76.4818
Ruminant Nutrition Laboratory	836 Campus Rd, Ithaca, NY 14850	42.4461, -76.4675
Ruth Bader Ginsburg Hall	155 Program House Dr, Ithaca, NY 14850	42.4544, -76.4758
S Barn	213 Farrier Rd, Ithaca, NY 14850	42.4482, -76.4638
S. T. Olin	162 Sciences Dr, Ithaca, NY 14850	42.4507, -76.4813
SPCA	1640 Hanshaw Rd, Ithaca, NY 14850	42.4720, -76.4386
Sage Chapel	147 Ho Plz, Ithaca, NY 14850	42.4472, -76.4845
Sage Hall	114 East Ave, Ithaca, NY 14850	42.4459, -76.4832
Sage House	118 Sage Pl, Ithaca, NY 14850	42.4397, -76.4915
Savage Hall	244 Garden Ave, Ithaca, NY 14850	42.4497, -76.4801
Sawdust Café (AgriTech)	33 Stone Barn Dr, Geneva, NY 14456	42.8767, -77.0016
Schoellkopf Field	145 Kite Hill Dr, Ithaca, NY 14850	42.4440, -76.4787
Schoellkopf House	521 Campus Rd, Ithaca, NY 14850	42.4450, -76.4792
Schoellkopf Memorial	521 Campus Rd, Ithaca, NY 14850	42.4450, -76.4786
Schurman Hall	602 Tower Rd, Ithaca, NY 14850	42.4480, -76.4661
Schwardt Laboratory	315 Turkey Hill Rd, Ithaca, NY 14850	42.4367, -76.4280
Schwartz Center for Performing Arts	430 College Ave, Ithaca, NY 14850	42.4424, -76.4859
Sculpture Garden	124 Comstock Knoll Dr, Ithaca, NY 14850	42.4519, -76.4551
Seal and Serpent Society	305 Thurston Ave, Ithaca, NY 14850	42.4535, -76.4856
Seed Processing (AgriTech)	21 Crabapple Dr, Geneva, NY 14456	42.8755, -77.0099
Seeley Mudd Hall	215 Tower Rd, Ithaca, NY 14850	42.4472, -76.4790
Sheldon Court	420 College Ave, Ithaca, NY 14850	42.4422, -76.4856
Sibley Hall	921 University Ave, Ithaca, NY 14850	42.4509, -76.4841
Sigma Alpha Mu	10 Sisson Place, Ithaca, NY 14850	42.4553, -76.4805
Sigma Chi	106 Cayuga Heights Rd., Ithaca, NY 14850	42.4567, -76.4912
Sigma Delta Tau	115 Ridgewood Rd., Ithaca, NY 14850	42.4561, -76.4885
Sigma Phi	1 Forest Park Lane, Ithaca, NY 14850	42.4460, -76.4885
Sigma Pi	730 University Avenue, Ithaca, NY 14850	42.4497, -76.4883
Snee Hall	112 Hollister Dr, Ithaca, NY 14850	42.4436, -76.4849
Space Sciences Building	122 Sciences Dr, Ithaca, NY 14850	42.4489, -76.4811
Spray Lab (AgriTech)	37 Castle Creek Dr, Geneva, NY 14456	42.8750, -77.0094
State Theatre	107 W State St, Ithaca, NY 14850	42.4394, -76.4996
Statler Auditorium	106 Statler Dr, Ithaca, NY 14850	42.4455, -76.4821
Statler Hall	106 Statler Dr, Ithaca, NY 14850	42.4458, -76.4822
Statler Hotel & J. Willard Marriott Executive Education Center	130 Statler Dr, Ithaca, NY 14853	42.4464, -76.4822
Stewart Park	1 James L Gibbs Dr, Ithaca, NY 14850	42.4621, -76.5018
Stimson Hall	204 East Ave, Ithaca, NY 14850	42.4478, -76.4833
Stocking Hall	411 Tower Rd, Ithaca, NY 14853	42.4472, -76.4712
Sturtevant Hall	630 W North St, Geneva, NY 14456	42.8766, -77.0067
Sturtevant Hall (AgriTech)	617 West North St, Geneva, NY 14456	42.8771, -77.0072
Surge 3 Facility	36 Judd Falls Rd, Ithaca, NY 14850	42.4460, -76.4702
Surge Laboratory (AgriTech)	101 Castle Creek Dr, Geneva, NY 14456	42.8750, -77.0094
Swanson Wildlife Health Center	131 Swanson Dr, Ithaca, NY 14850	42.4268, -76.4530
T Barn	205 Farrier Rd, Ithaca, NY 14850	42.4479, -76.4636
Taughannock Falls State Park	1740 Taughannock Blvd, Trumansburg, NY 14886	42.5465, -76.5985
Teagle Hall	512 Campus Rd, Ithaca, NY 14850	42.4458, -76.4791
Technion-Cornell Innovation Institute	2 West Loop Road, New York, NY 10044	40.7622, -73.9500
Telluride House	217 West Ave, Ithaca, NY 14850	42.4458, -76.4871
The Cornell Store	135 Ho Plz, Ithaca, NY 14850	42.4467, -76.4842
Theta Delta Chi	800 University Avenue, Ithaca, NY 14850	42.4501, -76.4877
Thurston Hall	130 Hollister Dr, Ithaca, NY 14850	42.4439, -76.4837
Tobin Field House	108 Jessup Rd, Ithaca, NY 14853	42.4565, -76.4810
Toboggan Lodge	38 Forest Home Dr, Ithaca, NY 14850	42.4512, -76.4786
Tompkins Co. Cooperative Extension	615 Willow Ave, Ithaca, NY 14850	42.4506, -76.5035
Tompkins County Public Library	101 East Green St, Ithaca, NY 14850	42.4384, -76.4984
Toni Morrison Hall	18 Sisson Pl, Ithaca, NY 14850	42.4554, -76.4797
Triphammer Road Cooperative	150 Triphammer Rd, Ithaca, NY 14850	42.4560, -76.4815
Turfgrass Field Research Lab	228 Bluegrass Ln, Ithaca, NY 14850	42.4596, -76.4608
USDA (AgriTech)	93 Collier Dr, Geneva, NY 14456	42.8762, -77.0082
USDA Screenhouse (AgriTech)	26 Innovation Blvd, Geneva, NY 14456	42.8574, -77.0349
Ujamaa Residential College	106 Northcross Rd, Ithaca, NY 14850	42.4553, -76.4767
Undergraduate Admissions Office	410 Thurston Ave, Ithaca, NY 14850	42.4539, -76.4843
Upson Hall	124 Hoy Rd, Ithaca, NY 14850	42.4439, -76.4821
Uris Hall	109 Tower Rd, Ithaca, NY 14850	42.4472, -76.4822
Uris Library	160 Ho Plz, Ithaca, NY 14850	42.4478, -76.4854
Vet Education Center	606 Tower Rd, Ithaca, NY 14850	42.4474, -76.4658
Vet Medical Center	930 Campus Rd, Ithaca, NY 14853	42.4474, -76.4644
Vet Research Tower	618 Tower Rd, Ithaca, NY 14850	42.4473, -76.4662
Von Cramm Hall	623 University Ave, Ithaca, NY 14850	42.4489, -76.4913
War Memorial	336 West Ave, Ithaca, NY 14850	42.4475, -76.4879
Ward Center for Nuclear Science	135 Hollister Dr, Ithaca, NY 14853	42.4434, -76.4830
Wari Cooperative	208 Dearborn Pl, Ithaca, NY 14850	42.4564, -76.4825
Warren Hall	137 Reservoir Ave, Ithaca, NY 14850	42.4492, -76.4771
Watermargin	103 McGraw Pl, Ithaca, NY 14850	42.4501, -76.4882
Weill Cornell Medical College	1300 York Ave, New York, NY 10065	40.7650, -73.9551
Weill Hall	237 Tower Rd, Ithaca, NY 14850	42.4469, -76.4775
White Hall	123 Central Ave, Ithaca, NY 14850	42.4503, -76.4854
Willard Straight Hall	136 Ho Plz, Ithaca, NY 14850	42.4465, -76.4856
Wilson Synchrotron Lab & Ring	161 Synchrotron Dr, Ithaca, NY 14850	42.4450, -76.4730
Wilson Synchrotron Lab Parking	161 Synchrotron Dr, Ithaca, NY 14850	42.4447, -76.4712
Wing Hall	123 Wing Dr, Ithaca, NY 14850	42.4466, -76.4716
Zeta Psi	534 Thurston Ave,. Ithaca, NY 14850	42.4541, -76.4818
Zucker Shrub Collection and Harris Lilac Collection	124 Comstock Knoll Dr, Ithaca, NY 14850	42.4526, -76.4561
104 West!	104 West Ave, Ithaca, NY 14850	42.4443, -76.4879
112 Edgemoor	112 Edgemoor Ln, Ithaca, NY 14850	42.4441, -76.4884
116 Maple Ave.	116 Maple Ave, Ithaca, NY 14850	42.4413, -76.4764
120 Maple Ave.	120 Maple Ave, Ithaca, NY 14850	42.4413, -76.4755
337 Pine Tree Road	337 Pine Tree Rd, Ithaca, NY 14850	42.4379, -76.4627
341 Pine Tree Road	341 Pine Tree Rd, Ithaca, NY 14850	42.4379, -76.4631
353 Pine Tree Road	353 Pine Tree Rd, Ithaca, NY 14850	42.4381, -76.4622
373 Pine Tree Road	373 Pine Tree Rd, Ithaca, NY 14850	42.4377, -76.4621
377 Pine Tree Road	377 Pine Tree Rd, Ithaca, NY 14850	42.4376, -76.4631
391 Pine Tree Road	391 Pine Tree Rd, Ithaca, NY 14850	42.4390, -76.4653
395 Pine Tree Road	395 Pine Tree Rd, Ithaca, NY 14850	42.4390, -76.4632
4-H Acres	418 Lower Creek Rd, Ithaca, NY 14850	42.4732, -76.4191
409 College Ave.	409 College Ave, Ithaca, NY 14850	42.4421, -76.4850
626 Thurston	626 Thurston Ave., Ithaca, NY14850	42.4518, -76.4809
726 University Ave.	726 University Ave, Ithaca, NY 14850	42.4496, -76.4888"""  # Truncated, assume full input is pasted here

# Split into lines
lines = raw_text.strip().split('\n')

location_map = {}

for line in lines:
    parts = line.split('\t')
    if len(parts) != 3:
        continue  # Skip malformed lines
    name, _, coords = parts
    lat_lng_match = re.match(r"([-+]?[0-9]*\.?[0-9]+),\s*([-+]?[0-9]*\.?[0-9]+)", coords)
    if lat_lng_match:
        lat, lng = lat_lng_match.groups()
        location_map[name.strip()] = {
            "name": name.strip(),
            "lat": float(lat),
            "lng": float(lng)
        }

# Save to JSON-like string for output
formatted_json = json.dumps(location_map, indent=2)
formatted_json[:1000]  # Only show preview
# Save to a file
with open('location-map.json', 'w') as f:
    json.dump(location_map, f, indent=2)

print("Saved as location-map.json")
