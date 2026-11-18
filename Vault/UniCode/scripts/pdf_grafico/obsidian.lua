-- Filtro pandoc: rende nel PDF grafico la sintassi di Obsidian usata negli appunti.
--   > [!tipo] Titolo      → <div class="callout tipo"> con titolo
--   > [!tipo]- Titolo     → come sopra (la piega di Obsidian nel PDF non serve)
--   [[nota]] / [[nota|x]] → testo in corsivo (nel PDF i collegamenti interni non portano da nessuna parte)

local function testo(inl)
  return pandoc.utils.stringify(inl)
end

function BlockQuote(bq)
  local primo = bq.content[1]
  if not primo or (primo.t ~= "Para" and primo.t ~= "Plain") then return nil end
  local inl = primo.content
  if #inl == 0 or inl[1].t ~= "Str" then return nil end
  local tipo, piega = inl[1].text:match("^%[!(%w+)%]([%-%+]?)$")
  if not tipo then return nil end

  -- titolo = resto della prima riga, fino al primo a capo
  local titolo, resto, i = {}, {}, 2
  while i <= #inl and inl[i].t ~= "SoftBreak" and inl[i].t ~= "LineBreak" do
    table.insert(titolo, inl[i]); i = i + 1
  end
  for j = i + 1, #inl do table.insert(resto, inl[j]) end
  while #titolo > 0 and titolo[1].t == "Space" do table.remove(titolo, 1) end

  local blocchi = {}
  if #titolo > 0 then
    table.insert(blocchi, pandoc.Div({ pandoc.Plain(titolo) }, pandoc.Attr("", { "callout-titolo" })))
  end
  local corpo = {}
  if #resto > 0 then table.insert(corpo, pandoc.Para(resto)) end
  for k = 2, #bq.content do table.insert(corpo, bq.content[k]) end
  table.insert(blocchi, pandoc.Div(corpo, pandoc.Attr("", { "callout-corpo" })))
  return pandoc.Div(blocchi, pandoc.Attr("", { "callout", tipo:lower() }))
end

function Link(l)
  if l.title == "wikilink" then
    return pandoc.Emph(l.content)
  end
end
