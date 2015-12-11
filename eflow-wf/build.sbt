lazy val commonSettings = Seq(
  organization := "eflow",
  version := "0.0.1-SNAPSHOT"
)

lazy val root = (project in file(".")).
  settings(commonSettings: _*).
  settings(
    name := "eflow-wf",
    libraryDependencies ++= Seq(
  	  "com.typesafe.slick" %% "slick" % "3.1.0" withSources() withJavadoc(),
  	  "com.typesafe.slick" %% "slick-extensions" % "3.1.0" withJavadoc(),
  	  "com.typesafe.akka" % "akka-actor_2.11" % "2.4.0",
  	  "com.typesafe.akka" % "akka-cluster_2.11" % "2.4.0",
      "org.slf4j" % "slf4j-nop" % "1.6.4" withSources() withJavadoc()
    ),
    resolvers += "Typesafe Releases" at "http://repo.typesafe.com/typesafe/maven-releases/"	
  )