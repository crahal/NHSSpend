addSbtPlugin("com.typesafe.play"         % "sbt-plugin"                % "2.8.1")
addSbtPlugin("org.portable-scala"        % "sbt-scalajs-crossproject"  % "1.0.0")
addSbtPlugin("com.typesafe.sbt"          % "sbt-gzip"                  % "1.0.2")
addSbtPlugin("com.typesafe.sbt"          % "sbt-digest"                % "1.1.4")

addSbtPlugin("com.vmunier"               % "sbt-web-scalajs"           % "1.0.11")
addSbtPlugin("org.scala-js"              % "sbt-scalajs"               % "1.0.0")

libraryDependencies += "org.vafer" % "jdeb" % "1.3" artifacts (Artifact("jdeb", "jar", "jar"))
