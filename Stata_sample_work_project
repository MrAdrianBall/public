
* Defines the 2020 geographic markets using a classification process based on distances from postcodes to flexpoints
**This classification process is based on the percentage of business sites within a buffer distance of X OCPs (as a base case).
**Various sensities are included, created by looping through global variables (base case is always first iteration).

clear all
set more off
set trace off
*local test = "\test"

global base "G:\1718-PR-002139 Telecoms Access Review 2020\LL Analysis\Network reach analysis"
global do "${base}\Do"
global input "${base}\Input"
global output "${base}\Output"
global circuit_data "G:\1718-PR-002139 Telecoms Access Review 2020\LL Analysis\Circuit data\output"

*Set up global and local macros
cd "${do}"
do "0a_Reference_NetworkReachMacrosGlobal.do"
include "0b_Reference_NetworkReachMacrosLocal.do"

*Load postcode area place names
cd "${input}"
import excel "PostCodeAreaNames (Wikipedia).xlsx", firstrow clear // AB 13/10/20 checked this file against latest Wikipedia list - still the same
rename (Postcodearea Postcodeareaname) (postarea postarea_name)
replace postarea_name = subinstr(postarea_name," ","_",20) // later this values will become variables (so we have to remove spaces) DF 15/01/20201
replace postarea_name = subinstr(postarea_name," ","_",20) // later this values will become variables (so we have to remove spaces) Note: this is not a duplicate
replace postarea_name = substr(postarea_name,1,16) // can't have more than 16 char, otherwise later can't become variable

tempfile postareas
save `postareas', replace

*Load cp access to network ratios
cd "${circuit_data}`test'"
foreach data_type in $circuits_data {
	local dtype = substr("`data_type'", 1, 1)
	foreach year in $year {
		use "cp_access_to_network_sites_ratio.dta", clear
		if "`data_type'" == "mnoinventory_access_ends_by_postcode" local year = "all"
		keep if connectionyear == "`year'" 
		keep cp `dtype'_access*
		tempfile `year'`dtype'_access_network_ratios 
		save ``year'`dtype'_access_network_ratios', replace 
	}
}

*Set up circuits data
foreach scen in $scenarios {
	foreach unit in $units {
		foreach data_type in $circuits_data {
		local dtype = substr("`data_type'", 1, 1)
			foreach uplift in $postcode_uplift {
				foreach year in $year {
					cd "${circuit_data}`test'"
					use "`data_type'.dta", clear
					if "`data_type'" == "mnoinventory_access_ends_by_postcode" local year = "all"
					keep if connectionyear == "`year'" 
					rename qty`scen' qty
					collapse (sum) qty, by(cp bwbucket postcode sector)
					replace bwbucket = "unknown" if bwbucket == ""
					rename bwbucket band
					drop if qty == .
					merge m:1 cp using ``year'`dtype'_access_network_ratios', keep(1 3) nogenerate 
					replace `dtype'_access_pc = 0 if `dtype'_access_pc == .
					replace `dtype'_access_nohull_pc = 0 if `dtype'_access_nohull_pc == .
					
					*Adjust cps' circuit ends with blank postcodes based on access to inter-exchange ratio
					replace qty = qty * (`dtype'_access_nohull_pc / 100) if `unit' == ""
					
					*Re-allocate CP's customer ends with blank postcodes among known postcodes
					if `uplift' == 1 {
						preserve	//add in area information so that uplift isn't applied in Hull
							cd "${input}`test'"
							use "ukpostcodes_2020classification.dta", clear
							keep `unit' area
							duplicates drop
							tempfile geo_areas
							save `geo_areas', replace
						restore
						merge m:1 `unit' using `geo_areas', keepusing(area) keep(1 3) nogenerate
						preserve
							gen qty_cp_blank = (`unit' == "") * qty
							gen qty_cp_non_blank = (`unit' != "" & area != "hull") * qty
							collapse (sum) qty_cp_blank qty_cp_non_blank, by(cp)
							gen ratio_cp_blank = qty_cp_blank / qty_cp_non_blank
							keep cp ratio_*
							tempfile cp_blank
							save `cp_blank', replace
						restore
						drop if `unit' == ""
						merge m:1 cp using `cp_blank', nogenerate
						replace ratio_cp_blank = 0 if ratio_cp_blank == . | area == "hull"
						replace qty = qty * (1 + ratio_cp_blank)
						drop ratio_* area
					}

					tempfile `scen'`dtype'`uplift'`unit'`year' 
					save ``scen'`dtype'`uplift'`unit'`year'', replace 
				}
			}
		}
	}
}

foreach fp in $flexpoint {
	*Set up postcode to flexpoint data for iterative use
	cd "${input}"
	use "post_`fp'_distances.dta", clear

	*Determine the number of OCPs within buffer distance of each postcode
	drop if cp == "openreach"	//ignored since we only consider OCPs with this metric
	foreach buff in $buffer_distances {
		gen ocps_`buff' = dist_ <= `buff'
	}

	collapse (sum) ocps_*, by(postcode postcode_split sector postarea area_2020)

	*Remove duplicate sectors, for the purposes of geographic matching
	bysort postcode (postcode_split): drop if _n > 1

	tempfile post_`fp'_dist
	save `post_`fp'_dist', replace
}

*Set up network sites data which will remove business sites coincident with network sites
if `net_sens' == 1 {
	cd "${input}"
	use "network_sites.dta", clear
	keep postcode
	duplicates drop
	tempfile net_sites
	save `net_sites', replace
}

foreach bus_thres in $business_thres {
	*Set up large business sites
	cd "${input}"
	use "business_sites.dta", clear
	rename no_businesses_`bus_thres' bus
	keep postcode bus
	if `net_sens' == 1 merge 1:1 postcode using `net_sites', keep(1) nogenerate
	tempfile business
	save `business', replace
	
	foreach scen in $scenarios {
		//Set up MNO sites, datacenters (customer side) and combine with business sites 
		cd "${circuit_data}`test'"
		use "mnoinventory_access_ends_by_postcode.dta", clear
		collapse (sum) qty`scen', by(postcode mno)
		gen mno_qty = (qty`scen' > 0)
		collapse (sum) mno_qty, by(postcode)
		merge 1:1 postcode using `business', nogenerate
		replace mno_qty = 0 if mno_qty == .
		replace bus = 0 if bus == .
		tempfile mnosites
		save `mnosites', replace
	
		preserve
			cd "${circuit_data}\temp\datacentres\"
			use "dc_list_customersite.dta", clear
			keep if customersite == "Y"
			gen dc_qty = 1
			collapse (sum) dc_qty, by(postcode) // assuming variables carrierowned/neutral/nocps2 are irrelevant here
			tempfile dcsitestemp
			save `dcsitestemp'
		restore
		merge 1:1 postcode using `dcsitestemp', nogen
		replace dc_qty = 0 if dc_qty == .
		replace bus = 0 if bus == .
		replace mno_qty = 0 if mno_qty== .
		tempfile allsites
		save `allsites'		

		foreach bus_inc in $include_bus {
			foreach mno_inc in $include_mno {
				foreach dc_inc in $include_dc {
					foreach cust_ends in $customer_ends {
						foreach uplift in $postcode_uplift {
							*Output combined bus/mno sites or customer ends based on sensitivity inclusion
							if "`cust_ends'" == "b" {
								use `allsites', clear
								gen bus_mno = (bus * `bus_inc') + (mno_qty * `mno_inc') + (dc_qty * `dc_inc')
							}
							if "`cust_ends'" == "c" {
								use ``scen'`cust_ends'`uplift'sector', clear
								collapse (sum) bus_mno = qty, by(postcode)
							}
							*keep postcode bus_mno
							rename (bus mno_qty bus_mno dc_qty) (no_bus no_mno bus no_dc)
							tempfile demand_sites
							save `demand_sites', replace

							foreach fp in $flexpoint {
								*Add in large business sites and MNO cell sites
								use `post_`fp'_dist', clear
								merge 1:1 postcode using `demand_sites', keep(1 3) nogenerate	//large business/MNO sites with no matching postcode are removed (NR calculation not possible with these)
								replace bus = 0 if bus == .
				
								*Reclassify no. of business sites if a sector has none
								egen sect_bus = total(bus), by(sector)
								replace bus = -1 if sect_bus == 0
								drop sect_bus
								
								*Weight postcodes with large business/MNO sites
								foreach buff in $buffer_distances {
									gen rivals_`buff' = ocps_`buff' * bus
								}
								
								tempfile sector_ocps
								save `sector_ocps', replace
				
								if `bus_thres' == `base_thres_bus'  & `scen' == `base_scen' & `bus_inc' == `base_bus_inc' & `mno_inc' == `base_mno_inc' & `dc_inc' == `base_dc_inc' & "`cust_ends'" == "`base_customer_ends'" & `uplift' == `base_postcode_uplift' /*& "`fp'" == "`base_flex'"*/ {	//base case scenario only (although NR bucket threshold doesn't affect these values in any case)
									replace bus = 0 if bus < 0
									preserve	//output no. of OCPs per postcode for separate calculations
										foreach buff in $buffer_distances {	//remove OCPs for no businesses classified areas
											replace rivals_`buff' = 0 if rivals_`buff' < 0
										}
										drop postarea area_2020
										local flex = substr("`fp'", 1, 2)
										cd "${input}`test'"
										save "nr_bus_`flex'.dta", replace
									restore
									if `mapping' == 1 {
										collapse (sum) ocps_50 bus, by(sector)	//unweighted no. of OCPs
										cd "${output}`test'"
										export delimited "sector_ocps_`fp'.csv", delimiter(",") replace
									}
								}
								
								foreach unit in $units {
									*Calculate weighted network reach per `unit'
									use `sector_ocps', clear
									collapse (sum) rivals_* bus, by(`unit' postarea area_2020)
									foreach buff in $buffer_distances {
										gen nr_`buff' = rivals_`buff' / bus
									}
									tempfile nr
									save `nr', replace
	
									*Determine percentage of business sites in each `unit' within X rivals
									use `sector_ocps', clear
									drop rivals_*
									reshape long ocps_, i(postcode* postarea sector bus area_2020) j(buff)
									collapse (sum) bus, by(`unit' postarea area_2020 ocps_ buff)
									preserve	//total no. of business sites per `unit'
										collapse (sum) bus, by(`unit' postarea area_2020 buff)
										rename bus bus_tot
										tempfile tot
										save `tot', replace
									restore
									merge m:1 `unit' postarea area_2020 buff using `tot', nogenerate
									gen bus_prop_ = bus / bus_tot
									reshape wide bus bus_prop_, i(`unit' postarea area_2020 buff bus_tot) j(ocps_)
									reshape long	//this pair of reshapes ensures that every `unit' has the full set of OCPs, for the purposes of cumulatives
									gsort `unit' postarea area_2020 buff -ocps_
									by `unit' postarea area_2020 buff: gen double bus_dcumprop_ = sum(bus_prop_)
									rename (bus bus_tot) (bus_ bus)
									quietly summarize ocps_*
									local max_2 = r(max)	//remember highest no. of OCPs for when classifying NR buckets
									reshape wide bus_*, i(`unit' postarea area_2020 buff bus) j(ocps_)
									foreach var of varlist bus_* {
										rename `var' `var'_
									}
									reshape wide bus_*, i(`unit' postarea area_2020 bus) j(buff)
									foreach var of varlist bus_* {
										replace `var' = 0 if `var' == .
									}
									
									*Add in average network reach
									merge 1:1 `unit' using `nr', keepusing(nr_*) nogenerate
									quietly summarize nr_*
									local max_1 = ceil(r(max))	//remember highest no. of OCPs for when classifying NR buckets
									tempfile nr_bus
									save `nr_bus', replace
									
									*Classify units into NR buckets based on either average network reach or percentage of business sites within X rivals
									foreach buck_thres in $nr_bucket_thres {
										foreach geo_meth in $geo_bucket_method {
											use `nr_bus', clear
											foreach buff in $buffer_distances {
												gen nr_bucket_flag_`buff' = .
												forvalues bucket = 0(1)`max_`geo_meth'' {
													if `geo_meth' == 1 replace nr_bucket_flag_`buff' = `bucket' if (nr_`buff' > (`bucket' - (1 - `buck_thres')) & nr_`buff' <= (`bucket' + `buck_thres') & nr_`buff' != .)
													if `geo_meth' == 2 replace nr_bucket_flag_`buff' = `bucket' if bus_dcumprop_`bucket'_`buff' >= `buck_thres'	//will overwrite until the highest no. of OCPs' bucket is found
													drop bus_`bucket'_`buff' bus_prop_`bucket'_`buff'
												}
												
												*Construct sector count variables based on NR bucket classification
												forvalues bucket = 0(1)`max_`geo_meth'' {
													gen or_`bucket'_`buff' = (nr_bucket_flag_`buff' == `bucket')
												}
												foreach cbucket in 2 6 {
													gen or_`cbucket'plus_`buff' = (nr_bucket_flag_`buff' >= `cbucket')
												}
												
												*"Reset" network reach values for sectors with no business sites
												replace nr_`buff' = 0 if bus < 0
											}
											replace bus = 0 if bus < 0
											
											*Store to separately count circuits
											tempfile `unit'
											save ``unit'', replace
											
											*Work out the no. of new connections per unit
											foreach cf_df_adj in $cf_dark_fibre_adj {
												local cfdfadj = `cf_df_adj'
												if `cf_df_adj' == 2/3 local cfdfadj = 67	//tempfile doesn't allow '/' in names
												if `cf_df_adj' == 0.95 local cfdfadj = 95	//tempfile doesn't allow '.' in names
												if `cf_df_adj' == 0.75 local cfdfadj = 75	//tempfile doesn't allow '.' in names
												foreach data_type in $circuits_data {
													local dtype = substr("`data_type'", 1, 1)
													foreach year in $year { 
														if "`data_type'" == "mnoinventory_access_ends_by_postcode" local year = "all"
														use ``scen'`dtype'`uplift'`unit'`year'', clear 
														
														*Removal adjustment of Cityfibre's dark fibre circuits
														cd "${output}`test'"
														collapse (sum) qty, by(band cp `unit')
														preserve	//work out no. of circuits that are being moved
															gen qty_cfdf = qty * `cf_df_adj' if band == "DF" & cp == "cityfibre"
															drop band qty
															drop if qty_cfdf == .
															replace qty_cfdf = qty_cfdf / 3	//split evenly between the 3 non-vhb bandwidths
															gen band = "0"
															foreach band in "10" "100" "1000" {
																replace band = "`band'"
																tempfile cfdf_`band'
																save `cfdf_`band'', replace
															}
														restore
														replace qty = qty * (1 - `cf_df_adj') if band == "DF" & cp == "cityfibre"	//remove DF circuits according to adjustment level
														foreach band in 10 100 1000 {	//add in circuits to each of the non-VHB bandwidths based on adjustment level
															merge 1:1 `unit' cp band using `cfdf_`band'', nogenerate
															replace qty = 0 if qty == .
															replace qty = qty + qty_cfdf if qty_cfdf != .
															drop qty_cfdf
														}
														
														*Determine the number of circuits for each unit per cp, bandwidth, and bandwidth group
														sort `unit' cp band
														quietly levelsof band, local(bands)
														quietly levelsof cp, local(cps)
														foreach band in `bands' {
															gen qty_`band' = (band == "`band'") * qty
															foreach cp in `cps' {
																gen qty_`band'_`cp' = (band == "`band'" & cp == "`cp'") * qty
															}
														}
														foreach cp in `cps' {
															gen qty_`cp' = (cp == "`cp'") * qty
															gen qty_nonvhb_`cp' = (cp == "`cp'" & (band == "10" | band == "100" | band == "1000")) * qty
															gen qty_vhb_df_`cp' = (cp == "`cp'" & (band == "VHB" | band == "DF")) * qty
														}
														gen qty_nonvhb = (band == "10" | band == "100" | band == "1000") * qty
														gen qty_vhb_df = (band == "VHB" | band == "DF") * qty
														collapse (sum) qty*, by(`unit')
											
														if `buck_thres' == `base_buck_thres' & `scen' == `base_scen' & `cf_df_adj' == `base_cf_df_adj' & `mapping' == 1 & `geo_meth' == `base_geo_meth' & `bus_thres' == `base_thres_bus' & `mno_inc' == `base_mno_inc' & `dc_inc' == `base_dc_inc' & "`data_type'" == "`base_data_type'" & "`cust_ends'" == "`base_customer_ends'" & "`fp'" == "`base_flex'" /* & "`year'" == "`base_year'"*/ {	//output service shares per unit for base case
															preserve
																foreach bandtype in "" "_nonvhb" "_VHB" "_vhb_df" {
																	gen share_or`bandtype' = qty`bandtype'_openreach / qty`bandtype'
																}
																keep `unit' share_or*
																rename *, lower
																export delimited "service_shares_map_`unit'_`year'.csv", delimiter(",") replace
															restore
														}
													
														gen scen = `scen'
														gen cfdfadj = `cfdfadj'
														gen geo_meth = `geo_meth'
														gen data_type = "`data_type'"
														gen postcode_uplift = `uplift'
														gen customer_ends = "`cust_ends'"
														gen flex = "`fp'"
														local flexp = substr("`fp'",1,2)
														gen year = "`year'"
														*tempfile con`unit'`scen'`cfdfadj'`geo_meth'`dtype'`uplift'`cust_ends'`flexp'`year'
														cd "${base}/tempfiles"
														save con`unit'`scen'`cfdfadj'`geo_meth'`dtype'`uplift'`cust_ends'`flexp'`year'.dta, replace
																												
														**Determine top city clusters - i.e. postcode areas (outside inner London) with highest no. of new connections in BT+>=2 sectors
														
														use ``unit'', clear
														*cd "${input}`test'"
														merge 1:1 `unit' using con`unit'`scen'`cfdfadj'`geo_meth'`dtype'`uplift'`cust_ends'`flexp'`year'.dta, nogenerate
														replace area_2020 = "invalid" if area_2020 == "" & `unit' != ""
														replace area_2020 = "unknown" if area_2020 == "" & `unit' == ""
														tempfile conarea
														save `conarea', replace
		
														foreach cbuff in $geo_buffer_distances {
															foreach top in $top_cities {
																use `conarea', clear
																
																*Redefine London areas as those units which are BT+>=2
																*replace area_2020 = "rouk" if area_2020 == "cla" & nr_bucket_flag_`cbuff' < 2
																*replace area_2020 = "rouk" if area_2020 == "cla" & nr_bucket_flag_`cbuff' < 2	//leaving this out ensures CLA is maintained
																
																drop if area_2020 == "cla" | area_2020 == "hull" | area_2020 == "unknown" | area_2020 == "invalid"	//leaves RoUK only
																tostring nr_bucket_flag_`cbuff', gen(nr_bucket_flag)
																replace nr_bucket_flag = "2plus" if nr_bucket_flag_`cbuff' >= 2 & nr_bucket_flag_`cbuff' != .
																
																*Determine clusters with highest number of connections (BT+>=2 bucket)
																preserve
																	collapse (sum) qty, by(nr_bucket_flag postarea)
																	keep if nr_bucket_flag == "2plus"
																	gsort -qty
																	gen toprank`top' = _n
																	gen toparea`top' = (toprank`top' <= `top')
																	tempfile toparea
																	save `toparea', replace
																restore
																
																*Flag sectors within top clusters which are in BT+>=2 bucket
																preserve
																	merge m:1 postarea using `toparea', keepusing(toparea`top' toprank`top') nogenerate
																	gen top`top' = (nr_bucket_flag == "2plus" & toparea`top' == 1)
																	tempfile clusters_`top'
																	save `clusters_`top'', replace
																restore
																
																*Feed clusters back into NR buckets data
																use ``unit'', clear
																merge 1:1 `unit' using `clusters_`top'', keepusing(top`top' toprank`top') nogenerate
																drop if nr_bucket_flag_`cbuff' == .
																
																*Redefine Inner London area as those units which are BT+>=2
																*replace area_2020 = "rouk" if area_2020 == "cla" & nr_bucket_flag_`cbuff' < 2
																*replace area_2020 = "rouk" if area_2020 == "cla" & nr_bucket_flag_`cbuff' < 2	//leaving this out ensures CLA is maintained
																
																*Recognise metro area if one of top cities
																merge m:1 postarea using `postareas', keep(1 3) nogenerate
																replace area_2020 = postarea_name if top`top' == 1
																replace toprank`top' = . if area_2020 == "rouk"
																drop postarea_name
																
																*Overlay NR buckets on geo areas
																replace area_2020 = "uk_bt_only" if area_2020 == "rouk" & nr_bucket_flag_`cbuff' == 0
																replace area_2020 = "uk_bt_plus1" if area_2020 == "rouk" & nr_bucket_flag_`cbuff' == 1
																replace area_2020 = "rouk_bt_2plus" if area_2020 == "rouk"
																
																gen double buck_thres = `buck_thres'
																gen scen = `scen'
																gen cfdfadj = `cfdfadj'
																gen cbuff = `cbuff'
																gen top = `top'
																gen geo_meth = `geo_meth'
																gen thres_bus = `bus_thres'
																gen bus_inc = `bus_inc'
																gen mno_inc = `mno_inc'
																gen dc_inc = `dc_inc'
																gen data_type = "`data_type'"
																gen postcode_uplift = `uplift'
																gen customer_ends = "`cust_ends'"
																gen flex = "`fp'"
																local flexp = substr("`fp'",1,2)
																gen year = "`year'" 
																local bt = `buck_thres' * 100
																local year_short = substr("`year'",-1,1) 
																cd "${base}/tempfiles"
																*tempfile geo`bt'`unit'`scen'`cfdfadj'`cbuff'`top'`geo_meth'`bus_thres'`bus_inc'`mno_inc'`dc_inc'`dtype'`uplift'`cust_ends'`flexp'`year_short' 
																save geo`bt'`unit'`scen'`cfdfadj'`cbuff'`top'`geo_meth'`bus_thres'`bus_inc'`mno_inc'`dc_inc'`dtype'`uplift'`cust_ends'`flexp'`year_short'.dta, replace  
																
																*Output geo markets
																if "`unit'" == "`base_unit'" & `scen' == `base_scen' & `cf_df_adj' == `base_cf_df_adj' & `top' == `base_top' & `bus_thres' == `base_thres_bus' & "`data_type'" == "`base_data_type'" & `uplift' == `base_postcode_uplift' & "`cust_ends'" == "`base_customer_ends'" & `bus_inc' == `base_bus_inc' & `mno_inc' == `base_mno_inc' & `dc_inc' == `base_dc_inc' /*& "year" == "base_year" & "`fp'" == "`base_flex'" */{	//base case (except geo (bucket threshold, buffer and method, bus/mno site inclusion)) Added MNO, DC and BUS filtering 3.02.2021 by DF
																	preserve
																		cd "${output}`test'"
																		drop if `unit' == "" | `unit' == "unknown" | `unit' == "invalid"
																		*replace area_2020 = "rouk_bt_2plus" if area_2020 == "cla"
																		keep `unit' area_2020 bus* nr* cbuff
																		drop bus_inc //UNCOMMENT OUT LINE 425
																		*export excel "`t_date'_`unit'_geo_areas_sensitivities.xlsx", sheet("`unit'_m`geo_meth'_t`buck_thres'_`cbuff'm_`bus_inc'`mno_inc'`dc_inc'") firstrow(variables) sheetreplace 
																		keep `unit' area_2020
																		local flexp = substr("`fp'",1,2)
																		export excel "`unit'_list_buff_geo_areas_`year'.xlsx", sheet("`unit'_m`geo_meth'_t`buck_thres'_`cbuff'm_`flexp'") firstrow(variables) sheetreplace  
																	restore
																}
																
																if `buck_thres' == `base_buck_thres' & "`unit'" == "`base_unit'" & `scen' == `base_scen' & `cf_df_adj' == `base_cf_df_adj' & `geo_meth' == `base_geo_meth' & `top' == `base_top' & `bus_thres' == `base_thres_bus' & `bus_inc' == `base_bus_inc' & `mno_inc' == `base_mno_inc' & `dc_inc' == `base_dc_inc' & "`data_type'" == "`base_data_type'" & `uplift' == `base_postcode_uplift' & "`cust_ends'" == "`base_customer_ends'" {	//base case except buffer distance
																	drop if `unit' == "" | `unit' == "unknown" | `unit' == "invalid"
																	keep `unit' area_2020 bus* nr* cbuff
																	drop bus_inc
																	cd "${input}`test'"
																	gen flex = "`fp'"
																	local flexp = substr("`fp'",1,2)
																	save "`unit'_geo_areas_`cbuff'm_`flexp'_`year'.dta", replace  
																	if "`fp'" == "`base_flex'" & "`year'" == "`base_year'" {	
																		*save "`unit'_geo_areas_`cbuff'm.dta", replace
																		*replace area_2020 = "rouk_bt_2plus" if area_2020 == "cla"
																		cd "${output}`test'"
																		local flexp = substr("`fp'",1,2)
																		if `mapping' == 1 export excel "`unit'_map_geo_areas_`year'.xlsx", sheet("`unit'_c`cbuff'm_`flexp'") firstrow(variables) sheetreplace 
																		keep `unit' area_2020
																		export excel "`unit'_list_geo_areas_`year'.xlsx", sheet("`unit'_c`cbuff'm_`flexp'") firstrow(variables) sheetreplace 
																		rename (sector area_2020) (Postcode_Sector Market)
																		replace Market = "CLA" if Market == "cla"
																		replace Market = "Hull Area" if Market == "hull"
																		replace Market = "HNR Areas" if Market == "Birmingham" | Market == "Bristol" | Market == "Glasgow" | Market == "Edinburgh" | Market == "Leeds" | Market == "Manchester" | Market == "Reading" | Market == "Slough" | Market == "South_East_Londo" | Market == "West_London" | Market == "Liverpool"
																		replace Market = "HNR Areas" if Market == "rouk_bt_2plus"
																		replace Market = "UK BT plus 1" if Market == "uk_bt_plus1"
																		replace Market = "UK BT only" if Market == "uk_bt_only"
																		if `legal_geo' == 1 export excel "`unit'_legal_geo_markets_`year'.xlsx", sheet("sectors_c`cbuff'm_`flexp'") firstrow(variables) sheetreplace  
																	}
																}
															}
														}											
													}
												}
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}
}
/*
cd "${input}`test'" // tempfiles weren't working we had to save them instead of create/append tempfiles
clear
*Save no. of new connections
foreach unit in $units {
	foreach cust_ends in $customer_ends {
		foreach uplift in $postcode_uplift {
			foreach geo_meth in $geo_bucket_method {
				foreach scen in $scenarios {
					foreach cf_df_adj in $cf_dark_fibre_adj {
						local cfdfadj = `cf_df_adj'
						if `cf_df_adj' == 2/3 local cfdfadj = 67	//tempfile doesn't allow '/' in names
						if `cf_df_adj' == 0.95 local cfdfadj = 95	//tempfile doesn't allow '.' in names
						if `cf_df_adj' == 0.75 local cfdfadj = 75	//tempfile doesn't allow '.' in names
						foreach data_type in $circuits_data {
							if "`data_type'" == "connections171819_access_ends_by_postcode" local dtype = "c"
							if "`data_type'" == "inventory2017_access_ends_by_postcode" local dtype = "i"
							if "`data_type'" == "mnoinventory_access_ends_by_postcode" local dtype = "m"
							foreach fp in $flexpoint {
							    if "`fp'" == "flexpoints" local flexp = "fl"
								if "`fp'" == "future_flexpoints" local flexp = "fu"
									foreach year in $year {  
										if "`data_type'" == "mnoinventory_access_ends_by_postcode" local year = "all"
										append using `con`unit'`scen'`cfdfadj'`geo_meth'`dtype'`uplift'`cust_ends'`flexp'`year''  
								}
							}
						}
					}
				}
			}
		}
	}
*/
	
	global contemps : dir "${base}/tempfiles" files "con*.dta"
	cd "${base}/tempfiles"
	
	clear 
	
	foreach dtafile of global contemps{
		append using `dtafile'
	}
	
	duplicates drop //mnoinventory has duplicates presumably as the three year scenarios are converted to "all"
	cd "${input}`test'"
	save "con_sector.dta", replace
*}

*Save areas dta file
/*foreach unit in $units { // tempfiles weren't working we had to save them instead of create/append tempfiles
	clear
	foreach bus_thres in $business_thres {
		foreach geo_meth in $geo_bucket_method {
			foreach scen in $scenarios {
				foreach bus_inc in $include_bus {
					foreach mno_inc in $include_mno {
						foreach dc_inc in $include_dc {
							foreach cust_ends in $customer_ends {
								foreach uplift in $postcode_uplift {
									foreach buck_thres in $nr_bucket_thres {
										local bt = `buck_thres' * 100
										foreach cf_df_adj in $cf_dark_fibre_adj {
											local cfdfadj = `cf_df_adj'
											if `cf_df_adj' == 2/3 local cfdfadj = 67	//tempfile doesn't allow '/' in names
											if `cf_df_adj' == 0.95 local cfdfadj = 95	//tempfile doesn't allow '.' in names
											if `cf_df_adj' == 0.75 local cfdfadj = 75	//tempfile doesn't allow '.' in names
											foreach data_type in $circuits_data {
												if "`data_type'" == "connections171819_access_ends_by_postcode" local dtype = "c"
												if "`data_type'" == "inventory2017_access_ends_by_postcode" local dtype = "i"
												if "`data_type'" == "mnoinventory_access_ends_by_postcode" local dtype = "m"
													foreach cbuff in $geo_buffer_distances {
														foreach top in $top_cities {
															foreach fp in $flexpoint {
																if "`fp'" == "flexpoints" local flexp = "fl"
																if "`fp'" == "future_flexpoints" local flexp = "fu"
																foreach year in $year {  
																	if "`data_type'" == "mnoinventory_access_ends_by_postcode" local year = "all"
																	local year_short = substr("`year'",-1,1)
																	append using `geo`bt'`unit'`scen'`cfdfadj'`cbuff'`top'`geo_meth'`bus_thres'`bus_inc'`mno_inc'`dc_inc'`dtype'`uplift'`cust_ends'`flexp'`year_short''  
															}
														}
													}
												}
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}
*/
	global geotemps : dir "${base}/tempfiles" files "geo*.dta"
	cd "${base}/tempfiles"
	
	clear 
	
	foreach dtafile of global geotemps{
		append using `dtafile'
	}
	
	cd "${input}`test'"
	save "areas_sector.dta", replace //replaced `unit' with sector
	

	

	
*}

do "${do}/3d_Analysis_GeoMarketClassification_WLA.do"
