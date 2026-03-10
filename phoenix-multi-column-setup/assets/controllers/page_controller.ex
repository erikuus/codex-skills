defmodule {{web_module}}.PageController do
  use {{web_module}}, :controller

  def home(conn, _params) do
    conn
    |> put_layout(html: {{{web_module}}.Layouts, :home})
    |> render(:home)
  end
end
