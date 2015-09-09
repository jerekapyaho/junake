(ns junake.web
  (:require [compojure.core :refer :all]
            [compojure.route :as route]
            [ring.middleware.defaults :refer [wrap-defaults site-defaults]]
            [cheshire.core :as json]))

(defroutes app-routes
  (GET "/" []
       {:status 200
        :headers {"Content-Type" "text/plain"}
        :body "Hello, world!"})
  (route/not-found "Not found"))

(def app
  (wrap-defaults app-routes site-defaults))
