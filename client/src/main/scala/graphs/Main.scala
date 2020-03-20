package graphs

import graphs.shared.SharedMessages
import org.scalajs.dom
import org.scalajs.dom.raw.{Element, Event, HTMLElement}

object Main {
	def anchorScroll(fragment: String): Unit = {
		val amount: Int = dom.document.getElementById("nav-header").clientHeight
		val ttarget: Element = dom.document.getElementById(fragment)
		ttarget match {
			case element: HTMLElement => if (element.offsetTop > 0) {
					//$('html,body').animate({ scrollTop: ttarget.offset().top - amount }, 250);
					//$(ttarget).animate({ scrollTop: ttarget.offset().top - amount }, 250);
				val scrolloffset: Double = element.offsetTop - amount
				dom.document.body.scrollTop = scrolloffset
				dom.document.documentElement.scrollTop = scrolloffset
			}
			case _ => println(ttarget)
		}
	}

	def scrollToWindowHash(event: Event): Unit = {
		if (dom.window.location.hash != "") {
			val fragment: String = dom.window.location.hash.substring(1)
			anchorScroll(fragment)
			event.preventDefault()
		}
	}

	def main(args: Array[String]): Unit = {
		//dom.document.getElementById("scalajsShoutOut").textContent = SharedMessages.itWorks
		dom.window.onload = scrollToWindowHash
		dom.window.onhashchange = scrollToWindowHash
	}
}