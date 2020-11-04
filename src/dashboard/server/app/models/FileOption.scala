package models

import com.typesafe.config.Config
import play.api.ConfigLoader._
import play.api.ConfigLoader

case class FileOption(filename: String, label: String)

object FileOption {
	implicit val fileConfigLoader: ConfigLoader[FileOption] = new ConfigLoader[FileOption] {
		def load(rootConfig: Config, path: String): FileOption = {
			FileOption(
				filename = rootConfig.getString("filename"),
				label = rootConfig.getString("label")
			)
		}
	}

	implicit val fileSeqConfigLoader: ConfigLoader[Seq[FileOption]] = new ConfigLoader[Seq[FileOption]] {
		def load(rootConfig: Config, path: String): Seq[FileOption] = {
			seqConfigLoader.load(rootConfig, path).map(c => fileConfigLoader.load(c))
		}
	}
}
