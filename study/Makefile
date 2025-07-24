#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
#  FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
#  WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

all:
	@echo "Targetes: clean check"

clean:
	rm -f *.pyc
	rm -rf __pycache__

check:
	@echo -n "Checking parser "
	@./pycomp.py -d 4 examples/add.pc    | grep "'num' '3' 0" >err
	@echo -n "."
	@./pycomp.py -d 4 examples/add2.pc   | grep "'num' '10' 0" >err
	@echo -n "."
	@./pycomp.py -d 4 examples/mul.pc    | grep "'num' '6' 0" >>err
	@echo -n "."
	@./pycomp.py -d 4 examples/expr.pc   | grep "'num' '7' 0" >>err
	@echo -n "."
	@./pycomp.py -d 4 examples/paren.pc  | grep "'num' '15' 0" >>err
	@echo -n "."
	@./pycomp.py -d 4 examples/paren2.pc | grep "'num' '25' 0" >>err
	@echo -n "."
	@./pycomp.py -d 4 examples/expr.pc   | grep "'num' '7' 0" >>err
	@echo -n "."
	@./pycomp.py -d 4 examples/expr2.pc  | grep "'num' '11' 0" >>err
	@echo " OK"

# End of Makefile
