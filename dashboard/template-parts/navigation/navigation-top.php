<nav id="nav-header" class="navbar navbar-expand-md navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow align-items-end">
	<a class="navbar-brand col-12 col-md-6 mr-0 mr-md-3" href="<?php echo get_bloginfo('url', 'display'); ?>">
		<h1 class="my-0 d-none d-md-block"><?php echo get_bloginfo('name', 'display'); ?></h1>
		<h1 class="my-0 h2 d-block d-md-none"><?php echo get_bloginfo('name', 'display'); ?></h1>
		<p class="text-truncate my-0"><?php bloginfo('description'); ?></p>
	</a>
	<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExampleDefault" aria-controls="navbarsExampleDefault" aria-expanded="false" aria-label="Toggle navigation">
		<span class="navbar-toggler-icon"></span>
	</button>

	<div class="collapse navbar-collapse align-items-end" id="navbarsExampleDefault">
		<ul class="navbar-nav mr-auto">
			<li class="nav-item<?php if ( is_front_page() ) : echo ' active'; endif; ?>">
				<a class="nav-link pl-1" href="<?php echo get_bloginfo('wpurl', 'display'); ?>"><span data-feather="home"></span><span class="ml-1">Home</span></a>
			</li>
			<li class="nav-item<?php if (get_post_field( 'post_name', get_post() ) == 'data'): echo ' active'; endif; ?>">
				<a class="nav-link pl-1" href="<?php echo get_permalink(get_page_by_path('dashboard', OBJECT, 'page')); ?>"><span data-feather="database"></span><span class="ml-1">Data</span><span class="sr-only"><?php if (get_post_field( 'post_name', get_post() ) == 'data'): echo '(current)'; endif; ?></span></a>
			</li>
			<li class="nav-item dropdown<?php $page = get_post_field( 'post_name', get_post() ); if (($page == 'project') || ($page == 'indicators') || ($page == 'team') || ($page == 'privacy-policy')): echo ' active'; endif; ?>">
				<a class="nav-link pl-1 dropdown-toggle" href="." id="dropdown01" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><span data-feather="info"></span><span class="ml-1">About</span></a>
				<div class="dropdown-menu" aria-labelledby="dropdown01">
					<a class="dropdown-item <?php if (get_post_field( 'post_name', get_post() ) == 'project'): echo 'active'; endif; ?>" href="<?php echo get_permalink(get_page_by_path('project', OBJECT, 'page')); ?>"><span data-feather="book-open"></span> Project</a>
					<a class="dropdown-item <?php if (get_post_field( 'post_name', get_post() ) == 'indicators'): echo 'active'; endif; ?>" href="<?php echo get_permalink(get_page_by_path('indicators', OBJECT, 'page')); ?>"><span data-feather="bar-chart-2"></span> Indicators</a>
					<a class="dropdown-item <?php if (get_post_field( 'post_name', get_post() ) == 'team'): echo 'active'; endif; ?>" href="<?php echo get_permalink(get_page_by_path('team', OBJECT, 'page')); ?>"><span data-feather="users"></span> Team</a>
					<a class="dropdown-item" href="mailto:digitalgendergaps@gmail.com?Subject=Digital%20Gender%20Gaps%20Project" target="_blank"><span data-feather="mail"></span> Contact Us</a>
					<a class="dropdown-item <?php if (get_post_field( 'post_name', get_post() ) == 'privacy-policy'): echo 'active'; endif; ?>" href="<?php echo get_permalink(get_page_by_path('privacy-policy', OBJECT, 'page')); ?>"><span data-feather="briefcase"></span> Privacy Policy</a>
				</div>
			</li>
		</ul>
		<span id="offlineIndicator" class="navbar-text px-3 display-5 d-none">Offline Mode</span>
	</div>
</nav>
