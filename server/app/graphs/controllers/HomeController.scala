package graphs.controllers

import java.io.File

import javax.inject._
import models.{FileOption, Image, Team}
import play.api._
import play.api.i18n._
import play.api.mvc._
import graphs.shared.SharedMessages
import play.api.libs.json.{JsError, JsPath, JsResult, JsSuccess, JsValue, Json}

/**
 * This controller creates an `Action` to handle HTTP requests to the
 * application's home page.
 */
@Singleton
class HomeController @Inject() (val controllerComponents: ControllerComponents, config: Configuration)(implicit webJarsUtil: org.webjars.play.WebJarsUtil) extends BaseController with I18nSupport {

	/**
	 * Create an Action to render an HTML page.
	 *
	 * The configuration in the `routes` file means that this method
	 * will be called when the application receives a `GET` request with
	 * a path of `/`.
	 */
	def index(): Action[AnyContent] = Action { implicit request: Request[AnyContent] =>
		Ok(views.html.index(SharedMessages.itWorks))
	}

	def coming_soon(): Action[AnyContent] = TODO

	def dash(): Action[AnyContent] = Action { implicit request: Request[AnyContent] =>
		//TODO should use the directory listing to filter for files present
		Environment.simple().getFile("server/public/data").listFiles()

		//TODO the config loader is a lot of boilerplate, fetching the node as a js object or string then json parsing would
		// allow use of the auto json convert and avoid the boilerplate
		val files: Seq[FileOption] = config.get[Seq[FileOption]]("graph_files")

		Ok(views.html.dashboard(files.toList))
	}

	def album(): Action[AnyContent] = Action { implicit request: Request[AnyContent] =>
		//TODO should use the directory listing to filter for files present
		//val filelist: Array[File] = Environment.simple().getFile("server/public/figs/capacity_plots").listFiles()
		//val files = filelist.map(i => Image(controllers.covid_19_server.routes.Assets.versioned(i.getPath), i.getPath, i.getPath))
		//val files = filelist.map(i => Image((i.getName), i.getName, i.getName))
		//import com.typesafe.config.Config
		//import play.api.ConfigLoader._
		//import play.api.ConfigLoader
		//implicit val imageReads = Json.reads[Image]
		val files: Seq[Image] = config.get[Seq[Image]]("graph_files")


		// In a request, a JsValue is likely to come from `request.body.asJson`
		// or just `request.body` if using the `Action(parse.json)` body parser
		//val jsonString: JsValue = Json.parse(files.head.getAnyRef(""))

		//val residentFromJson: JsResult[Image] = Json.fromJson[Image](jsonString)

		//residentFromJson match {
		//	case JsSuccess(f: Image, path: JsPath) => Ok(views.html.album(List(f)))
		//	case e: JsError => Ok("Errors: " + JsError.toJson(e).toString())
		//}
		Ok(views.html.album(files.toList))

	}

	def about(): Action[AnyContent] = TODO

	def donut(): Action[AnyContent] = Action { implicit request: Request[AnyContent] =>
		val files: Seq[FileOption] = config.get[Seq[FileOption]]("graph_files")
		Ok(views.html.donut(files.toList))
	}

	def project(): Action[AnyContent] = Action { implicit request: Request[AnyContent] =>
		Ok(views.html.project())
	}

	def team(): Action[AnyContent] = Action { implicit request: Request[AnyContent] =>
		Ok(views.html.team(Team.people))
	}

	def privacy(): Action[AnyContent] = TODO
}
