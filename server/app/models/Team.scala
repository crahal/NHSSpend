package models

import controllers.routes

object Team {
	val people: List[TeamMember] = List(
		new TeamMember("Michelle Degli Esposti", "PostDoctoral Research Fellow\n" +
			"Michelle is the principal investigator leading on this work to provide the first monitoring tool for measuring child maltreatment in the UK and examining patterns over time. Michelle completed her D.Phil on examining the risks of child maltreatment at the individual and societal level. She is now working as a postdoctoral research fellow at the Department of Social Policy and Intervention, University of Oxford." +
			"", routes.Assets.versioned("images/mde.jpg"), List(
			new Link("user", "https://www.spi.ox.ac.uk/people/michelle-degli-esposti", "contact details")
		)),
		new TeamMember("Cheryl Koh", "Research Assistant\n" +
			"Cheryl is supporting the project as Research Assistant. She helps identify and screen datasets that support the data tool, and co-ordinates subsequent data requests and ethics approvals.\n\n\n\nCheryl is currently a graduate student in the Department of Social Policy and Intervention. She is interested in the population health consequences of experiencing excessive stress (‘toxic stress’) in childhood and adolescence as a result of maltreatment, and interventions aiming to improve child and maternal health. Prior to Oxford, Cheryl had worked closely with government and not-for-profit child protection organisations in Australia as a management consultant." +
			"", routes.Assets.versioned("images/cheryl.png"), List()
		),
		new TeamMember("Ian Knowles", "DevOp\n" +
			"Ian is a freelance data engineer with an academic background and wide-ranging experience in industry. He has development experience in most major languages and has worked on projects that range from embedded device firmware and applications, to desktop and mobile applications, and on to full stack web server development and operations.\n" +
			"He developed the website backend, frontend, and data visualisations", routes.Assets.versioned("images/ian.jpg"), List(
			new Link("github", "https://github.com/ianknowles", "ianknowles")
		))
	)
}
