					<div class="d-flex justify-content-between align-items-end flex-wrap pb-2 mb-3">
						<div class="btn-toolbar mt-2 mb-0 mr-sm-2 flex-column flex-lg-row">
							<div class="input-group m-1">
								<div class="input-group-prepend">
									<label for="<?php echo get_query_var('map-template-id'); ?>-select-tab" class="input-group-text">
										<span class="sr-only">Model prediction picker for map</span><span data-feather="folder"></span>
									</label>
								</div>
								<select id="<?php echo get_query_var('map-template-id'); ?>-select-tab" class="custom-select btn-outline-secondary h-100" data-style="btn-primary">
									<option value="data/csv1_tab2.csv">Coverage</option>
									<option value="data/csv2_tab2.csv">Reconciled supplies</option>
								</select>
							</div>
							<div class="input-group m-1">
								<div class="input-group-prepend">
									<label for="<?php echo get_query_var('map-template-id'); ?>-report-picker" class="input-group-text">
										<span class="sr-only">Report picker</span><span data-feather="calendar"></span>
									</label>
								</div>
								<select id="<?php echo get_query_var('map-template-id'); ?>-report-picker" class="custom-select btn-outline-secondary h-100" data-style="btn-primary">
									<option value="latest">Latest<span class="spinner-border spinner-border-sm"></span></option>
									<option value="latest">2018-05</option>
									<option value="latest">2018-06-05</option>
								</select>
							</div>
							<div class="input-group m-1">
								<div class="input-group-prepend">
									<label for="<?php echo get_query_var('map-template-id'); ?>-select-column" class="input-group-text">
										<span class="sr-only">Model prediction picker for map</span><span data-feather="bar-chart-2"></span>
									</label>
								</div>
								<select id="<?php echo get_query_var('map-template-id'); ?>-select-column" class="custom-select btn-outline-secondary h-100" data-style="btn-primary">
									<option value="Number_Payments_to_Companies">Company payments</option>
									<option value="Value_Payments_to_Companies">Amount paid to companies</option>
									<option value="Number_Payments_to_Charites">Charity payments</option>
									<option value="Value_Payments_to_Charites">Amount paid to charities</option>
								</select>
							</div>
							<div class="btn-group btn-group-sm m-1">
								<button
									id="<?php echo get_query_var('map-template-id'); ?>-sharemail"
									type="button"
									class="btn btn-outline-secondary d-flex"
									href="mailto:?to=&body=,&subject="
									target="_blank"
								>
									<div class="m-1"><span data-feather="mail"></span></div>
									<div class="m-1">Share</div>
								</button>
								<button
									id="<?php echo get_query_var('map-template-id'); ?>-csvlink"
									type="button"
									class="btn btn-outline-secondary d-flex"
								>
									<div class="m-1">Export</div>
									<div class="m-1"><span data-feather="download"></span></div>
								</button>
							</div>
						</div>
					</div>
