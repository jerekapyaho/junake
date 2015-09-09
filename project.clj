(defproject junake "1.0.0-SNAPSHOT"
  :description "Proxy for the rata.digitraffic.fi service"
  :url "https://github.com/jerekapyaho/junake"
  :license {:name "MIT License"
            :url "http://opensource.org/licenses/MIT"}
  :dependencies [[org.clojure/clojure "1.6.0"]
                 [compojure "1.3.1"]
                 [ring/ring-defaults "0.1.2"]
                 [environ "0.5.0"]]
  :min-lein-version "2.0.0"
  :plugins [[lein-ring "0.8.13"]]
  :ring {:handler junake.web/app}
  :uberjar-name "junake-standalone.jar"
  :profiles {:dev {:dependencies [[javax.servlet/servlet-api "2.5"]]}})
