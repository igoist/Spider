(ns huaban.core
  (:require [org.httpkit.client :as http]
            [clojure.java.io :as io]
            [clojure.data.json :as json])
  (:gen-class))

(def image-save-path "./img/")

(defn get-home-page
  "get homepage"
  []
  (let [options {:timeout 1000
                 :as :text}
        url "http://huaban.com/favorite/geek"
        {:keys [body]} @(http/get url options)]
    body))

(defn get-image-info
  "从首页内容得到图片信息"
  [page]
  (subs (re-find (re-matcher #"page\[\"pins\"\].*;" page)) 15))

(defn str2json
  "transfer str of json to dist"
  [body]
  (json/read-str body :key-fn keyword))

(defn download-image
  "save single/1 img to locale"
  [url file-name]
  (println (str "downloading " url))
  (with-open [in (io/input-stream url)
              out (io/output-stream file-name)]
    (io/copy in out)))

(defn make-image-url
  "get the real path of img by the key value"
  [k]
  (str "http://hbimg.b0.upaiyun.com/" k "_fw658")) ; 236?

(defn make-file-name
  [file-name]
  (str image-save-path file-name ".jpg"))

(defn download-images
  "download multiple imgs with json"
  [jsons
   (dorun (map (fn [a]
                (let [k (:key (:file a)) file-name (:pin_id a)]
                  (download-image (make-image-url k) (make-file-name file-name))))
              jsons))]
  (:pin_id (last jsons)))

(defn download-home-page
  "start to download"
  []
  (-> (get-home-page)
      get-image-info
      str2json
      download-images))


;; part 2
(defn make-json-request-url
  "根据pin值创建Ajax请求url"
  [pin]
  (str "http://huaban.com/favorite/beauty/?is07k6hx&max=" pin "&limit=20&wfl=1"))

(defn get-more-page
  "load ajax requests"
  [last-pin]
  (let [options {:timeout 1000
                 :as :text
                 :header {"Accept" "application/json"
                          "X-Request-With" "XMLHttpRequest"
                          "X-Request" "JSON"}}
        {:keys [body]} @(http/get (make-json-request-url last-pin) options)]
    body))

(defn download-more
  "img with ajax/afterhomepage"
  [last-pin]
  (-> last-pin
      get-more-page
      str2json
      second
      second
      download-images))

(defn main
  "下载指定页数的图片，如果不指定页数，下载首页图片"
  ([]
   (download-home-page)
   (println "Finished"))
  ([page-num]
   (if (> 1 page-num)
     (download-home-page)
     (letfn [(down-more
               [pin n]
               (println pin)
               (if (zero? n)
                 (println "Finished!")
                 (recur (download-more pin) (dec n))))]
       (down-more (download-home-page) (- page-num 1))))))



(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (println "Hello, World!"))

(if 1
  (println 1)
  (println 0))
