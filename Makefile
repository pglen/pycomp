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
	rm -f *.pyc
	rm -rf __pycache__
	rm err

git:
	git add .
	git commit -m autocheck
	git push

# Decide on one or the other
ERR=/dev/null
#ERR=err

# This is a simple send / expect for quick checking parser

check:
	@echo -n "Checking parser "
	@./pycomp.py examples/add.pc       | grep "'num' '3' 0" >${ERR}
	@echo -n "."
	@./pycomp.py examples/add2.pc      | grep "'num' '10' 0" >>${ERR}
	@echo -n "."
	@./pycomp.py examples/mul.pc       | grep "'num' '6' 0" >>${ERR}
	@echo -n "."
	@./pycomp.py examples/mul2.pc      | grep "'num' '24' 0" >>${ERR}
	@echo -n "."
	@./pycomp.py  examples/expr.pc     | grep "'num' '7' 0" >>${ERR}
	@echo -n "."
	@./pycomp.py  examples/expr2.pc    | grep "'num' '11' 0" >>${ERR}
	@echo -n "."
	@./pycomp.py examples/paren.pc     | grep "'num' '15' 0" >>${ERR}
	@echo -n "."
	@./pycomp.py examples/paren2.pc    | grep "'num' '25' 0" >>${ERR}
	@echo -n "."
	@./pycomp.py  examples/paren3.pc   | grep "'num' '15' 0" >>${ERR}
	@echo -n "."
	@./pycomp.py  examples/paren4.pc   | grep "'num' '11' 0" >>${ERR}
	@echo " OK"

lexcheck:
	@echo -n "."
	@./pycomp.py -x examples/comm2.pc  | grep "Another"  >>${ERR}
	@echo -n "."
	@./pycomp.py -x examples/comm3.pc  | grep "comment \"here\""  >>${ERR}
	@echo -n "."
	@./pycomp.py -x examples/comm4.pc  | grep "Doc Comment"  >>${ERR}
	@echo -n "."
	@./pycomp.py -x examples/str.pc    | grep "Hello World"  >>${ERR}
	@echo -n "."
	@./pycomp.py -x examples/str2.pc   | grep "hello 'old' world"  >>${ERR}
	@echo -n "."
	@./pycomp.py -x examples/str3.pc   | grep "hello world" >>${ERR}
	@echo -n "."
	@./pycomp.py -x examples/str5.pc   | grep "hello world: 1234 AB :; again " >>${ERR}

	@echo " OK"

# End of Makefile
