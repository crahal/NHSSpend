package controllers

import javax.inject._
import models.Team
import play.api._
import play.api.i18n._
import play.api.mvc._

/**
 * This controller creates an `Action` to handle HTTP requests to the
 * application's home page.
 */
@Singleton
class HomeController @Inject()(val controllerComponents: ControllerComponents)(implicit webJarsUtil: org.webjars.play.WebJarsUtil) extends BaseController with I18nSupport {

	/**
	 * Create an Action to render an HTML page.
	 *
	 * The configuration in the `routes` file means that this method
	 * will be called when the application receives a `GET` request with
	 * a path of `/`.
	 */
	def index(): Action[AnyContent] = Action { implicit request: Request[AnyContent] =>
		Ok(views.html.index())
	}

	def dash(): Action[AnyContent] = Action { implicit request: Request[AnyContent] =>
		Ok(views.html.dashboard())
	}

	def about(): Action[AnyContent] = TODO

	def project(): Action[AnyContent] = Action { implicit request: Request[AnyContent] =>
		Ok(views.html.project())
	}

	def team(): Action[AnyContent] = Action { implicit request: Request[AnyContent] =>
		Ok(views.html.team(Team.people))
	}

	def privacy(): Action[AnyContent] = TODO
}
