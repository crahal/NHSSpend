<!-- //TODO min height set to force the scrollbar, set the empty sizes more realistically -->
					<figure class="position-relative map-contain">
						<div id="<?php echo get_query_var('map-template-id'); ?>-shade" class="map-shade background-color-sea position-absolute w-100 h-100 d-flex justify-content-center align-items-center"><span class="spinner-border"></span></div>
						<div class="row" >
							<div class="col-12 col-lg-11 d-lg-flex flex-lg-column pr-lg-0">
								<div id="<?php echo get_query_var('map-template-id'); ?>-chart-area" class="border background-color-sea"></div>
							</div>
							<?php get_template_part('template-parts/graph/graph', 'legend-v'); ?>
						</div>
						<?php
							get_template_part('template-parts/graph/graph', 'legend-h');
							get_template_part('template-parts/graph/graph', 'palettepicker');
						?>
						<figcaption class="sr-only">Prediction map</figcaption>
					</figure>
