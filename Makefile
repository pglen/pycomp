#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
#  FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
#  WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

.PHONY: clean check

all:
	@echo "Targetes: clean check git"

clean:
	@rm -f *.pyc
	@rm -rf __pycache__
	@rm -f err
	@rm -rf tmp/*

git:
	git add .
	git commit -m autocheck
	git push

# This is a simple send / expect for quick checking parser

check:
	@testvdrive.py testcase.txt
	@#testvdrive.py testexpr.txt

# End of Makefile
