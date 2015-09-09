(ns junake.web
  (:require [compojure.core :refer :all]
            [compojure.route :as route]
            [ring.middleware.defaults :refer [wrap-defaults site-defaults]]
            [clojure.java.io :as io]
            [ring.middleware.stacktrace :as trace]
            [ring.middleware.session :as session]
            [ring.middleware.session.cookie :as cookie]
            [ring.adapter.jetty :as jetty]
            [environ.core :refer [env]]))

(defroutes app-routes
  (GET "/" []
       {:status 200
        :headers {"Content-Type" "text/plain"}
        :body "Hello, world!"})
  (route/not-found "Not found"))

(def app
  (wrap-defaults app-routes site-defaults))
