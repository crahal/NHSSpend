<?php
	get_header();
	get_template_part('template-parts/navigation/navigation', 'top');
?>
<div class="container-fluid position-absolute top-0 h-100">
	<div class="row h-100">
		<?php get_sidebar(); ?>
		<main role="main" class="col-12 col-md-10 ml-sm-auto px-0">
			<div class="d-flex flex-column justify-content-between h-100 px-0">
				<div class="px-4">
					<div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
						<h1 id="comparison" class="h2">Comparison</h1>
						<div class="btn-toolbar mb-2 mb-md-0">
							<label for="reportpicker" class="sr-only">Report picker</label>
							<select class="selectpicker btn btn-sm btn-outline-secondary mr-2 ml-auto my-1" data-style="btn-primary" id="reportpicker"
									onchange="change_report()">
								<option value="latest">Latest</option>
							</select>
							<label for="selCol1" class="sr-only">Model prediction picker for map</label>
							<select class="selectpicker btn btn-sm btn-outline-secondary mr-2 ml-auto my-1" data-style="btn-primary" id="selCol1"
									onchange="changeColumn1()"></select>
							<div class="btn-group ml-auto mr-2 my-1">
								<!--<button class="btn btn-sm btn-outline-secondary" onclick="csvshare()">Share</button>-->
								<a id="sharemail" href="mailto:?to=&body=,&subject=" class="btn btn-sm btn-outline-secondary" target="_blank"><span data-feather="mail"></span> Share</a>
								<a id="csvlink" class="btn btn-sm btn-outline-secondary"
								   href="#">Export <span data-feather="download"></span></a>
							</div>
							<!--<button class="btn btn-sm btn-outline-secondary dropdown-toggle">
								<span data-feather="calendar"></span>
								<select id="selCol2" onchange="changeColumn2()"></select>
							</button>-->
						</div>
					</div>


			<!--<div class="container" style="width:100vh; height:68vh">
				<div class="row">
					<div class="col">
						<div>
							<select class="selectpicker btn btn-sm btn-outline-secondary" data-style="btn-primary" id="fileSel1">
								<option>2018-05</option>
							</select>
							<select class="selectpicker btn btn-sm btn-outline-secondary" data-style="btn-primary" id="selCol1" onchange="changeColumn1()"></select>
						</div>
						<div id="container1" style="position: relative;"></div>
					</div>
					<div class="col">
						<div>
							<select class="selectpicker btn btn-sm btn-outline-secondary" data-style="btn-primary" id="fileSel2">
								<option>2018-05</option>
							</select>
							<select class="selectpicker btn btn-sm btn-outline-secondary" data-style="btn-primary" id="selCol2" onchange="changeColumn2()"></select>
						</div>
						<div id="container2" style="position: relative;"></div>
					</div>
				</div>
			</div>-->
					<figure style="min-height: 25vw"><!-- embed-responsive embed-responsive-2by1 -->
						<div class="row" ><!-- embed-responsive-item -->
							<div class="col-11" ><div id="container1" style="background:LightCyan"></div></div>
							<div id="map-legend" class="col-1"></div>
						</div>
					<figcaption class="sr-only">Prediction map</figcaption></figure>
					<figure style="min-height: 25vw"><!-- embed-responsive embed-responsive-2by1 -->
						<div class="row" ><!-- embed-responsive-item -->
							<div class="col-11" ><div id="container2" style="background:LightCyan"></div></div>
							<div id="map-legend" class="col-1"></div>
						</div>
					<figcaption class="sr-only">Prediction map</figcaption></figure>

					<div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
						<h2>Details</h2>
						<div class="btn-toolbar mb-2 mb-md-0">
							<!--<span data-feather='filter'></span>-->
							<form class="form-inline my-2 my-lg-0">
								<input id='search' class="form-control mr-sm-2" type="text" placeholder="Filter by Country" aria-label="Filter">
								<!--<button class="btn btn-outline-success my-2 my-sm-0" type="submit">Filter</button>-->
							</form>
						</div>
					</div>
					<!-- TODO min height set to force the scrollbar -->
					<div class="table-responsive" style="min-height: 100vh">
						<table class="table table-striped table-sm" id="modeltable">
						</table>
					</div>
				</div>
				<div class="mt-2">
					<?php get_template_part('template-parts/footer/footer', 'authorship'); ?>
				</div>
			</div>
		</main>
	</div>
</div>
<script type="application/json" id="formdata">
{
	"report1": "<?php echo filter_input(INPUT_GET, 'report1'); ?>"
	"report2": "<?php echo filter_input(INPUT_GET, 'report2'); ?>"
}
</script>
<?php
	get_template_part('template-parts/footer/footer', 'keyscripts');
	get_template_part('template-parts/footer/footer', 'graphscripts');
	get_footer();
?>
