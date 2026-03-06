defmodule {{app_module}}.MultiColumn.Spec do
  defstruct [:app_module, :web_module, :otp_app, :auth_mode, :spec_path, groups: []]

  defmodule Group do
    defstruct [
      :key,
      :label,
      :icon,
      :layout_name,
      :session_name,
      :menu_module,
      :layout_file,
      :menu_file,
      :live_dir,
      items: []
    ]
  end

  defmodule Item do
    defstruct [
      :kind,
      :key,
      :label,
      :icon,
      :path,
      :aliases,
      :section,
      :expandable_id,
      :relative_module,
      :full_module,
      :live_file,
      :dom_id,
      :parent_labels,
      children: []
    ]
  end
end
