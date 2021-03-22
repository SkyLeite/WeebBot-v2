defmodule Admin.Guild do
  @moduledoc """
  The Guild context.
  """

  import Ecto.Query, warn: false
  alias Admin.Repo

  alias Admin.Guild.AvailableSetting

  @doc """
  Returns the list of available_settings.

  ## Examples

      iex> list_available_settings()
      [%AvailableSetting{}, ...]

  """
  def list_available_settings do
    Repo.all(AvailableSetting)
  end

  @doc """
  Gets a single available_setting.

  Raises `Ecto.NoResultsError` if the Available setting does not exist.

  ## Examples

      iex> get_available_setting!(123)
      %AvailableSetting{}

      iex> get_available_setting!(456)
      ** (Ecto.NoResultsError)

  """
  def get_available_setting!(id), do: Repo.get!(AvailableSetting, id)

  @doc """
  Creates a available_setting.

  ## Examples

      iex> create_available_setting(%{field: value})
      {:ok, %AvailableSetting{}}

      iex> create_available_setting(%{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def create_available_setting(attrs \\ %{}) do
    %AvailableSetting{}
    |> AvailableSetting.changeset(attrs)
    |> Repo.insert()
  end

  @doc """
  Updates a available_setting.

  ## Examples

      iex> update_available_setting(available_setting, %{field: new_value})
      {:ok, %AvailableSetting{}}

      iex> update_available_setting(available_setting, %{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def update_available_setting(%AvailableSetting{} = available_setting, attrs) do
    available_setting
    |> AvailableSetting.changeset(attrs)
    |> Repo.update()
  end

  @doc """
  Deletes a available_setting.

  ## Examples

      iex> delete_available_setting(available_setting)
      {:ok, %AvailableSetting{}}

      iex> delete_available_setting(available_setting)
      {:error, %Ecto.Changeset{}}

  """
  def delete_available_setting(%AvailableSetting{} = available_setting) do
    Repo.delete(available_setting)
  end

  @doc """
  Returns an `%Ecto.Changeset{}` for tracking available_setting changes.

  ## Examples

      iex> change_available_setting(available_setting)
      %Ecto.Changeset{data: %AvailableSetting{}}

  """
  def change_available_setting(%AvailableSetting{} = available_setting, attrs \\ %{}) do
    AvailableSetting.changeset(available_setting, attrs)
  end
end
