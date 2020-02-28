package models

import play.api.mvc.Call

class Person(val name: String, val desc: String, val imageurl: Call, val links: List[Link]) {}
