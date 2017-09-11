include Nanoc::Helpers::Blogging
include Nanoc::Helpers::Rendering

module InlineHelper
  def inline (identifier, other_assigns = {}, &block)
    raise Exception unless identifier.start_with? '/'
    File.read('content/' + identifier)
  end
end

use_helper InlineHelper
