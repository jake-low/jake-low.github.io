def excerpt (item)
  content = item.compiled_content
  if content =~ /\s<!-- MORE -->\s/
    content.partition('<!-- MORE -->').first
  else
    content
  end
end
