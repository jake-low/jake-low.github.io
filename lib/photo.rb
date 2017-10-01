def pretty_exif (path)
  exif = JSON.parse(`exiftool -All -j content/#{path}`)[0]

  attributes = {
    :title => exif['Title'] || exif['Caption'],
    :date => Date::strptime(exif['CreateDate'], '%Y:%m:%d %H:%M:%S'),

    :focal_length => exif['FocalLength'],
    :aperture => exif['Aperture'],
    :shutter_speed => exif['ExposureTime'],
    :iso => exif['ISO'],
    :aspect => exif['ImageWidth'].to_f / exif['ImageHeight'].to_f,
  }

  make = exif['Make']
  model = exif['Model']

  attributes[:camera] = model.start_with?(make) ? model : "#{make} #{model}"

  if attributes[:camera] == 'DJI FC220'
    attributes[:camera] = 'DJI Mavic Pro'
  end

  attributes[:lens] = exif['LensModel']

  location = [ exif['Sub-location'], exif['City'], exif['Province-State'], exif['Country'] ]
  location.compact!
  # de-duplicate adjacent location names e.g. "Hanoi, Hanoi" => "Hanoi"
  deduped_location = location.chunk{|e| e}.map(&:first)
  attributes[:location] = deduped_location.join ', '

  attributes[:sublocation] = exif['Sub-location']
  attributes[:city] = exif['City']
  attributes[:province_state] = exif['Province-State']
  attributes[:country] = exif['Country']

  attributes
end

class Convert < Nanoc::Filter
  identifier :convert
  type       :binary

  def run(filename, params = {})
    args = []
    args.push('-resize', params[:size].to_s) if params[:size]
    args.push('-quality', params[:quality].to_s) if params[:quality]

    # puts 'CONVERTING'
    # puts filename
    # puts output_filename

    # puts "convert #{args.join(' ')} #{filename} #{output_filename}"
    # puts `convert #{args.join(' ')} #{filename} #{output_filename}`

    system('convert', *args, filename, output_filename)
  end
end

class BinaryToTextHack < Nanoc::Filter
  identifier :bin2txt
  type :binary => :text

  def run(filename, params = {})
    return ""
  end
end
