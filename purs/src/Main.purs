module Main where

import Prelude
import Control.Monad.Eff (Eff)
import Control.Monad.Eff.Console (CONSOLE, log)
import DOM (DOM())
import DOM.HTML (window)
import DOM.HTML.Types (htmlDocumentToDocument)
import DOM.HTML.Window (document)
import DOM.Node.NonElementParentNode (getElementById)
import DOM.Node.Types (Element(), Document(), ElementId(..),
                       documentToNonElementParentNode)
import Data.Maybe (Maybe(), fromJust)
import Data.Nullable (toMaybe)
import Partial.Unsafe (unsafePartial)

-- DOM helpers from https://github.com/sharkdp/cube-composer
getDocument :: forall eff. Eff (dom :: DOM | eff) Document
getDocument = window >>= document <#> htmlDocumentToDocument

getElementById' :: forall eff. String
                -> Document
                -> Eff (dom :: DOM | eff) (Maybe Element)
getElementById' id doc = do
  let docNode = documentToNonElementParentNode doc
  nullableEl <- getElementById (ElementId id) docNode
  pure $ toMaybe nullableEl

foreign import setInnerHTML :: forall eff. String -> Element -> Eff (dom :: DOM | eff) Unit

unsafeFromJust :: forall a. Maybe a -> a
unsafeFromJust = unsafePartial fromJust

greetingWords :: String
greetingWords = "Hello world!"

main :: forall e. Eff (dom :: DOM, console :: CONSOLE | e) Unit
main = do
  doc <- getDocument
  content <- unsafeFromJust <$> getElementById' "content" doc
  setInnerHTML ("<h1>" <> greetingWords <> "</h1>") content
  log greetingWords
