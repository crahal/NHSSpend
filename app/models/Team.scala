package models

import controllers.routes

object Team {
	val people: List[Person] = List(
		new Person("Michelle Degli Esposti", "PostDoctoral Research Fellow\n" +
			"Michelle is the principal investigator leading on this work to provide the first monitoring tool for measuring child maltreatment in the UK and examining patterns over time. Michelle completed her D.Phil on examining the risks of child maltreatment at the individual and societal level. She is now working as a postdoctoral research fellow at the Department of Social Policy and Intervention, University of Oxford." +
			"", routes.Assets.versioned("images/mde.jpg"), List(
			new Link("user", "https://www.spi.ox.ac.uk/people/michelle-degli-esposti", "contact details")
		)),
		new Person("Ian Knowles", "DevOp\n" +
			"Ian is a freelance data engineer with an academic background and wide-ranging experience in industry. He has development experience in most major languages and has worked on projects that range from embedded device firmware and applications, to desktop and mobile applications, and on to full stack web server development and operations.\n" +
			"He developed the website backend, frontend, and data visualisations", routes.Assets.versioned("images/ian.jpg"), List(
			new Link("github", "https://github.com/ianknowles", "ianknowles")
		))
	)
}
