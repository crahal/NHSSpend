package models

import play.api.mvc.Call

case class TeamMember(name: String, desc: String, imageurl: Call, links: List[Link])
