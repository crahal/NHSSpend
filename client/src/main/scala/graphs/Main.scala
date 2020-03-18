package graphs

import graphs.shared.SharedMessages
import org.scalajs.dom

object Main {

	def main(args: Array[String]): Unit = {
		dom.document.getElementById("scalajsShoutOut").textContent = SharedMessages.itWorks
	}
}