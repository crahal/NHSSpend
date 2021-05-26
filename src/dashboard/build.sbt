name := """nhsspenddash"""

version := "1.0-SNAPSHOT"

// Adds additional packages into Twirl
//TwirlKeys.templateImports += "com.example.controllers._"

// Adds additional packages into conf/routes
// play.sbt.routes.RoutesKeys.routesImport += "com.example.binders._"

lazy val nhsdash_server = (project in file("server"))
	.settings(commonSettings)
	.settings(
		scalaJSProjects := Seq(nhsdash_client, nhsdash_clientGraphing),
		pipelineStages in Assets := Seq(scalaJSPipeline),
		pipelineStages := Seq(digest, gzip),
		// triggers scalaJSPipeline when using compile or continuous compilation
		compile in Compile := ((compile in Compile) dependsOn scalaJSPipeline).value,
		libraryDependencies ++= Seq(
			"com.vmunier" %% "scalajs-scripts" % "1.1.4",
			guice,
			specs2 % Test,
			"org.scalatestplus.play" %% "scalatestplus-play" % "5.0.0" % Test,
			"org.webjars" %% "webjars-play" % "2.8.0",
			"org.webjars" % "bootstrap" % "4.4.1",
			"org.webjars" % "d3js" % "5.9.7",
			"org.webjars.npm" % "topojson" % "3.0.2",
			"org.webjars" % "jquery" % "3.4.1",
			"org.webjars" % "popper.js" % "1.15.0",
			"org.webjars" % "c3" % "0.6.6",
			"org.webjars.npm" % "feather-icons" % "4.24.1",
			"com.typesafe.play" %% "play-slick" % "4.0.2",
			"com.typesafe.play" %% "play-slick-evolutions" % "4.0.2",
			"com.h2database" % "h2" % "1.4.199",
),
		maintainer in Linux := "Ian Knowles <ian@imknowles.co.uk>",
		packageSummary in Linux := "Webserver for nhs spend data",
		packageDescription := "Webserver for nhs spend data",
		debianPackageDependencies := Seq("openjdk-11-jre-headless"),
	)
	.enablePlugins(PlayScala, JDebPackaging)
	.dependsOn(nhsdash_sharedJvm)

lazy val nhsdash_client = (project in file("client"))
	.settings(commonSettings)
	.settings(
		scalaJSUseMainModuleInitializer := true,
		mainClass in compile := Some("graphs.Main"),
		libraryDependencies ++= Seq(
			"org.scala-js" %%% "scalajs-dom" % "1.0.0"
		),
	)
	.enablePlugins(ScalaJSPlugin, ScalaJSWeb)
	.dependsOn(nhsdash_sharedJs)

lazy val nhsdash_clientGraphing = (project in file("clientGraphing"))
	.settings(commonSettings)
	.settings(
		scalaJSUseMainModuleInitializer := true,
		mainClass in compile := Some("graphs.Graphing"),
		libraryDependencies ++= Seq(
			"org.scala-js" %%% "scalajs-dom" % "1.0.0"
		),
	)
	.enablePlugins(ScalaJSPlugin, ScalaJSWeb)
	.dependsOn(nhsdash_sharedJs)

lazy val nhsdash_shared = crossProject(JSPlatform, JVMPlatform)
	.crossType(CrossType.Pure)
	.in(file("shared"))
	.settings(commonSettings)
lazy val nhsdash_sharedJvm = nhsdash_shared.jvm
lazy val nhsdash_sharedJs = nhsdash_shared.js

lazy val commonSettings = Seq(
	scalaVersion := "2.13.1",
	organization := "com.imknowles",
	scalacOptions ++= Seq(
		"-feature",
		"-deprecation",
		"-Xfatal-warnings",
		"-target:11"
	),
	javacOptions ++= Seq("-target", "11")
)

// loads the server project at sbt startup
onLoad in Global := (onLoad in Global).value.andThen(state => "project nhsdash_server" :: state)