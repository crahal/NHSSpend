<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	<meta name="description" content="<?php bloginfo('description'); ?>" />
	<meta name="author" content="<?php the_author_meta( 'display_name', get_post_field( 'post_author', get_queried_object_id() ) ); ?>">
	<meta name="generator" content="WordPress">
	<meta name="keywords" content="gender inequality, development indicators, internet access, data science, sociology, research, facebook data, global gender gap report">
	<meta property="og:title" content="<?php echo get_post_field( 'post_title', get_post() ); ?>" />
	<meta property="og:description" content="<?php bloginfo('description'); ?>" />
	<meta property="og:site_name" content="<?php echo get_bloginfo('name', 'display'); ?>" />
	<meta property="og:type" content="website" />
	<meta property="og:url" content="<?php echo get_permalink()?>" />
	<!-- //TODO include a default in the theme and an option for upload -->
	<meta property="og:image" content="https://www.digitalgendergaps.org/wp-content/uploads/2018/10/report_screenshot.png" />
	<link rel="icon" type="image/gif" href="<?php echo get_theme_file_uri('/assets/images/Icons-mini-icon_world.gif'); ?>">
	<!-- //TODO deprecated -->
	<title><?php wp_title(' | ', true, 'right'); ?><?php echo get_bloginfo('name', 'display'); ?></title>

	<!-- Bootstrap core CSS -->
	<link href="<?php echo get_theme_file_uri('/assets/css/vendor/bootstrap.min.css'); ?>" rel="stylesheet">
	<link href="<?php echo get_theme_file_uri('/assets/css/vendor/c3.min.css'); ?>" rel="stylesheet">

	<!-- Custom styles for this template -->
	<link href="<?php echo get_theme_file_uri('/assets/css/dashboard.css'); ?>" rel="stylesheet">
	<link href="<?php echo get_stylesheet_uri(); ?>" rel="stylesheet">

	<link rel="manifest" href="<?php echo get_theme_file_uri('manifest.json'); ?>">
	<?php wp_head(); ?>
</head>
<body>
