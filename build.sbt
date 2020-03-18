name := """childhoodmaltreatment"""

version := "1.0-SNAPSHOT"

// Adds additional packages into Twirl
//TwirlKeys.templateImports += "com.example.controllers._"

// Adds additional packages into conf/routes
// play.sbt.routes.RoutesKeys.routesImport += "com.example.binders._"

lazy val server = (project in file("server"))
	.settings(commonSettings)
	.settings(
		scalaJSProjects := Seq(client),
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
			"org.webjars" % "jquery" % "3.4.1",
			"org.webjars" % "popper.js" % "1.15.0",
			"org.webjars" % "c3" % "0.6.6",
			"org.webjars.npm" % "feather-icons" % "4.24.1",
		),
		maintainer in Linux := "Ian Knowles <ian@imknowles.co.uk>",
		packageSummary in Linux := "Webserver for C Protect",
		packageDescription := "Webserver for C Protect",
		debianPackageDependencies := Seq("openjdk-11-jre-headless"),
	)
	.enablePlugins(PlayScala, JDebPackaging)
	.dependsOn(sharedJvm)

lazy val client = (project in file("client"))
	.settings(commonSettings)
	.settings(
		scalaJSUseMainModuleInitializer := true,
		mainClass in compile := Some("graphs.Main"),
		libraryDependencies ++= Seq(
			"org.scala-js" %%% "scalajs-dom" % "1.0.0"
		),
	)
	.enablePlugins(ScalaJSPlugin, ScalaJSWeb)
	.dependsOn(sharedJs)

lazy val shared = crossProject(JSPlatform, JVMPlatform)
	.crossType(CrossType.Pure)
	.in(file("shared"))
	.settings(commonSettings)
lazy val sharedJvm = shared.jvm
lazy val sharedJs = shared.js

lazy val commonSettings = Seq(
	scalaVersion := "2.13.1",
	organization := "com.imknowles"
)

// loads the server project at sbt startup
onLoad in Global := (onLoad in Global).value.andThen(state => "project server" :: state)
