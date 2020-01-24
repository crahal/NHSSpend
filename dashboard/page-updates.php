<?php
	get_header();
	get_template_part('template-parts/navigation/navigation', 'top');
?>
<div class="container-fluid position-absolute top-0 h-100">
	<div class="row h-100">
		<?php get_sidebar(); ?>
		<main role="main" class="col-12 col-md-10 ml-sm-auto px-0">
			<div class="d-flex flex-column justify-content-between h-100 px-0">
				<div class="p-4">
					<?php $catquery = new WP_Query( 'cat=2&posts_per_page=5' ); ?>
					<?php while($catquery->have_posts()) : $catquery->the_post(); ?>
					<div class="card my-4">
						<div class="card-header"><h4><?php echo get_the_date(); ?></h4></div><div class="card-body"><h3 class="card-title"><a href="<?php the_permalink() ?>" rel="bookmark"><?php the_title(); ?></a></h3>
						<p class="card-text"><?php the_content(); ?></p></div>
					</div>
					<?php endwhile; ?>
					<?php wp_reset_postdata(); ?>
				</div>
				<div class="mt-2">
					<?php get_template_part('template-parts/footer/footer', 'authorship'); ?>
				</div>
			</div>
		</main>
	</div>
</div>
<?php
	get_template_part('template-parts/footer/footer', 'keyscripts');
	get_footer();
?>
