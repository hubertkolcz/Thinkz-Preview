require 'tempfile'

module Equation
  def self.parse(sgcink_data)
    # raise InvalidPathDataError unless sgcink_data.to_s.match?(/^SCG_INK(\n\d+(\s\d+)?)*$/)
    output = seshat_file(sgcink_data)
    raise SeshatError, output if output.match?(/Error/i)
    output
  end

  # def self.seshat_file(data)
  #   file = File.open('/home/lyon106/web/seshat/SampleMathExps/exp.scgink', 'w')
  #   file.write(data)
  #   result = `/home/lyon106/web/seshat/seshat -c /home/lyon106/web/seshat/Config/CONFIG -i /home/lyon106/web/seshat/SampleMathExps/exp.scgink | tail -n 1`
  #   result.strip
  # end

  # #{file.path}
  # /home/lyon106/web/seshat/SampleMathExps/exp.scgink
  def self.seshat_file(data)
    File.truncate('/home/lyon106/web/seshat/SampleMathExps/expression.scgink', 0)
    File.open('/home/lyon106/web/seshat/SampleMathExps/expression.scgink', 'w') { |file| file.write(data) }
    File.write('/home/lyon106/web/seshat/SampleMathExps/expression.scgink', data, mode: 'a')
    result = `/home/lyon106/web/seshat/seshat -c /home/lyon106/web/seshat/Config/CONFIG -i /home/lyon106/web/seshat/SampleMathExps/exp.scgink | tail -n 1`
    result.strip
  end

  class InvalidPathDataError < StandardError; end
  class SeshatError < StandardError; end
end
