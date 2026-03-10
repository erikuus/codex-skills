defmodule {{web_module}}.ErrorHTML do
  use {{web_module}}, :html

  embed_templates "error_html/*"

  def render(template, _assigns) do
    Phoenix.Controller.status_message_from_template(template)
  end
end
