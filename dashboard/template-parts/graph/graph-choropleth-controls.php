					<div class="d-flex justify-content-between align-items-end flex-wrap pb-2 mb-3 border-bottom">
						<div class="flex-column">
							<div><h1 class="h2 my-0">Report</h1></div>
							<div id="<?php echo get_query_var('map-template-id'); ?>-report-label"><h2 class="h3 my-0"></h2><span class="spinner-border"></span></div>
						</div>
						<div class="btn-toolbar mt-2 mb-0 mr-sm-2 flex-column flex-lg-row">
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
									<option value="Ground Truth Internet GG">Internet GG - ITU</option>
									<option value="Internet online model prediction">Internet GG - Online</option>
									<option value="Internet Online-Offline model prediction">Internet GG - Combined</option>
									<option value="Internet Offline model prediction">Internet GG - Offline</option>
									<option value="Mobile_GG">Mobile GG - GSMA</option>
									<option value="Mobile Online model prediction">Mobile GG - Online</option>
									<option value="Mobile Online-Offline model prediction">Mobile GG - Combined</option>
									<option value="Mobile Offline model prediction">Mobile GG - Offline</option>
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
