<!-- //TODO min height set to force the scrollbar, set the empty sizes more realistically -->
					<figure class="position-relative">
						<div id="<?php echo get_query_var('map-template-id'); ?>-shade" class="map-shade background-color-sea position-absolute w-100 h-100 d-flex justify-content-center align-items-center"><span class="spinner-border"></span></div>
						<div class="row" style="min-height: 50px;">
							<div class="col-12" style="min-height: 50px;">
								<div id="<?php echo get_query_var('map-template-id'); ?>-chart-area" class="border background-color-sea h-100 c3"  style="min-height: 500px;"></div>
							</div>
						</div>
						<?php
							get_template_part('template-parts/graph/graph', 'legend-h');
							//get_template_part('template-parts/graph/graph', 'palettepicker');
						?>
						<figcaption id="<?php echo get_query_var('map-template-id'); ?>-chart-caption" class="text-light"></figcaption>
					</figure>
