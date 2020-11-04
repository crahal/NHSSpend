package models

import com.typesafe.config.Config
import play.api.ConfigLoader
import play.api.ConfigLoader._

case class Image(src: String, desc: String, alt: String)

object Image {
	implicit val fileConfigLoader: ConfigLoader[Image] = new ConfigLoader[Image] {
		def load(rootConfig: Config, path: String): Image = {
			Image(
				src = rootConfig.getString("src"),
				desc = rootConfig.getString("desc"),
				alt = rootConfig.getString("alt")
			)
		}
	}

	implicit val fileSeqConfigLoader: ConfigLoader[Seq[Image]] = new ConfigLoader[Seq[Image]] {
		def load(rootConfig: Config, path: String): Seq[Image] = {
			seqConfigLoader.load(rootConfig, path).map(c => fileConfigLoader.load(c))
		}
	}
}