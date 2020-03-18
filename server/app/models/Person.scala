package models

import play.api.mvc.Call

case class Person(name: String, desc: String, imageurl: Call, links: List[Link])
