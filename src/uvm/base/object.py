#
#-----------------------------------------------------------------------------
# Copyright 2007-2014 Mentor Graphics Corporation
# Copyright 2014 Semifore
# Copyright 2010-2018 Synopsys, Inc.
# Copyright 2007-2018 Cadence Design Systems, Inc.
# Copyright 2010-2012 AMD
# Copyright 2013-2018 NVIDIA Corporation
# Copyright 2017-2018 Cisco Systems, Inc.
# Copyright 2017 Verific
# Copyright 2019 Matthew Ballance
#   All Rights Reserved Worldwide
#
#   Licensed under the Apache License, Version 2.0 (the
#   "License"); you may not use this file except in
#   compliance with the License.  You may obtain a copy of
#   the License at
#
#       http:#www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in
#   writing, software distributed under the License is
#   distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#   CONDITIONS OF ANY KIND, either express or implied.  See
#   the License for the specific language governing
#   permissions and limitations under the License.
#-----------------------------------------------------------------------------


#------------------------------------------------------------------------------
#
# CLASS -- NODOCS -- uvm_object
#
# The uvm_object class is the base class for all UVM data and hierarchical 
# classes. Its primary role is to define a set of methods for such common
# operations as <create>, <copy>, <compare>, <print>, and <record>. Classes
# deriving from uvm_object must implement the pure virtual methods such as 
# <create> and <get_type_name>.
#
#------------------------------------------------------------------------------

# @uvm-ieee 1800.2-2017 auto 5.3.1
class uvm_object(uvm_void):
    
    m_inst_count = 0


    # Function -- NODOCS -- new
    #
    # Creates a new uvm_object with the given instance ~name~. If ~name~ is not
    # supplied, the object is unnamed.

    def __init__ (self, name=""):
        super().__init__()
        self.m_inst_id = self.m_inst_count
        self.m_inst_count += 1
        self.m_leaf_name = name


    # Group -- NODOCS -- Seeding

    # Function -- NODOCS -- get_uvm_seeding

    # @uvm-ieee 1800.2-2017 auto 5.3.3.1
    @staticmethod
    def get_uvm_seeding(self):
        cs = uvm_core_service_t.get()
        return cs.get_uvm_seeding()
      
    # Function -- NODOCS -- set_uvm_seeding

    # @uvm-ieee 1800.2-2017 auto 5.3.3.2
    @staticmethod
    def set_uvm_seeding(self, enable):
        cs = uvm_core_service_t.get()
        cs.set_uvm_seeding(enable)
        
    # Function -- NODOCS -- reseed
    #
    # Calls ~srandom~ on the object to reseed the object using the UVM seeding
    # mechanism, which sets the seed based on type name and instance name instead
    # of based on instance position in a thread. 
    #
    # If <get_uvm_seeding> returns 0, then reseed() does
    # not perform any function. 

    # @uvm-ieee 1800.2-2017 auto 5.3.3.3
    def reseed(self):
        if self.uvm_get_seeding():
            self.srandom(uvm_create_random_seed(get_type_name(), get_full_name()))


    # Group -- NODOCS -- Identification

    # Function -- NODOCS -- set_name
    #
    # Sets the instance name of this object, overwriting any previously
    # given name.

    # @uvm-ieee 1800.2-2017 auto 5.3.4.1
    def set_name(self, name):
        self.m_leaf_name = name


    # Function -- NODOCS -- get_name
    #
    # Returns the name of the object, as provided by the ~name~ argument in the
    # <new> constructor or <set_name> method.

    # @uvm-ieee 1800.2-2017 auto 5.3.4.2
    def get_name(self):
        return self.m_leaf_name

    # Function -- NODOCS -- get_full_name
    #
    # Returns the full hierarchical name of this object. The default
    # implementation is the same as <get_name>, as uvm_objects do not inherently
    # possess hierarchy. 
    #
    # Objects possessing hierarchy, such as <uvm_components>, override the default
    # implementation. Other objects might be associated with component hierarchy
    # but are not themselves components. For example, <uvm_sequence #(REQ,RSP)>
    # classes are typically associated with a <uvm_sequencer #(REQ,RSP)>. In this
    # case, it is useful to override get_full_name to return the sequencer's
    # full name concatenated with the sequence's name. This provides the sequence
    # a full context, which is useful when debugging.

    # @uvm-ieee 1800.2-2017 auto 5.3.4.3
    def get_full_name(self):
        return self.get_name()


    # Function -- NODOCS -- get_inst_id
    #
    # Returns the object's unique, numeric instance identifier.

    # @uvm-ieee 1800.2-2017 auto 5.3.4.4
    def get_inst_id(self):
        return self.m_inst_id
        


    # Function -- NODOCS -- get_inst_count
    #
    # Returns the current value of the instance counter, which represents the
    # total number of uvm_object-based objects that have been allocated in
    # simulation. The instance counter is used to form a unique numeric instance
    # identifier.
    @staticmethod
    def get_inst_count():
        return uvm_object.m_inst_count


    # Function -- NODOCS -- get_type
    #
    # Returns the type-proxy (wrapper) for this object. The <uvm_factory>'s
    # type-based override and creation methods take arguments of
    # <uvm_object_wrapper>. This method, if implemented, can be used as convenient
    # means of supplying those arguments.
    #
    # The default implementation of this method produces an error and returns
    # ~null~. To enable use of this method, a user's subtype must implement a
    # version that returns the subtype's wrapper.
    #
    # For example:
    #
    #|  class cmd (uvm_object):;
    #|    typedef uvm_object_registry #(cmd) type_id;
    #|    static function type_id get_type();
    #|      return type_id::get();
    #|    endfunction
    #|  endclass
    #
    # Then, to use:
    #
    #|  factory.set_type_override(cmd::get_type(),subcmd::get_type());
    #
    # This function is implemented by the `uvm_*_utils macros, if employed.
    @staticmethod
    def get_type(self):
        # TODO: error handling
        # uvm_report_error("NOTYPID", "get_type not implemented in derived class.", UVM_NONE);
        return None


    # Function -- NODOCS -- get_object_type
    #
    # Returns the type-proxy (wrapper) for this object. The <uvm_factory>'s
    # type-based override and creation methods take arguments of
    # <uvm_object_wrapper>. This method, if implemented, can be used as convenient
    # means of supplying those arguments. This method is the same as the static
    # <get_type> method, but uses an already allocated object to determine
    # the type-proxy to access (instead of using the static object).
    #
    # The default implementation of this method does a factory lookup of the
    # proxy using the return value from <get_type_name>. If the type returned
    # by <get_type_name> is not registered with the factory, then a ~null~
    # handle is returned.
    #
    # For example:
    #
    #|  class cmd (uvm_object):;
    #|    typedef uvm_object_registry #(cmd) type_id;
    #|    static function type_id get_type();
    #|      return type_id::get();
    #|    endfunction
    #|    virtual function type_id get_object_type();
    #|      return type_id::get();
    #|    endfunction
    #|  endclass
    #
    # This function is implemented by the `uvm_*_utils macros, if employed.

    def get_object_type(self):
        cs = uvm_core_service_t.get()
        factory = cs.get_factory()
        
        if self.get_type_name() == "<unknown>":
            return None
        
        return factory.find_wrapper_by_name(self.get_type_name())


    # Function -- NODOCS -- get_type_name
    #
    # This function returns the type name of the object, which is typically the
    # type identifier enclosed in quotes. It is used for various debugging
    # functions in the library, and it is used by the factory for creating
    # objects.
    #
    # This function must be defined in every derived class. 
    #
    # A typical implementation is as follows:
    #
    #|  class mytype (uvm_object):;
    #|    ...
    #|    static function string type_name(); return "myType"; endfunction : type_name
    #|
    #|    virtual function string get_type_name();
    #|      return type_name;
    #|    endfunction
    #
    # We define the ~type_name~ static method to enable access to the type name
    # without need of an object of the class, i.e., to enable access via the
    # scope operator, ~mytype::type_name~.

    def get_type_name(self):
        return "<unknown>"

    # Group -- NODOCS -- Creation

    # Function -- NODOCS -- create
    #
    # The ~create~ method allocates a new object of the same type as this object
    # and returns it via a base uvm_object handle. Every class deriving from
    # uvm_object, directly or indirectly, must implement the create method.
    #
    # A typical implementation is as follows:
    #
    #|  class mytype (uvm_object):;
    #|    ...
    #|    virtual function uvm_object create(string name="");
    #|      mytype t = new(name);
    #|      return t;
    #|    endfunction 

    def create(self, name=""):
        return None

  
    # Function -- NODOCS -- clone
    #
    # The ~clone~ method creates and returns an exact copy of this object.
    # 
    # The default implementation calls <create> followed by <copy>. As clone is
    # virtual, derived classes may override this implementation if desired. 

    # @uvm-ieee 1800.2-2017 auto 5.3.5.2
    def clone(self):
        tmp = self.create(self.get_name())
        if tmp is None:
            # TODO: error handling
            # uvm_report_warning("CRFLD", $sformatf("The create method failed for %s,  object cannot be cloned", get_name()), UVM_NONE);
            pass
        else:
            tmp.copy(self)
        return tmp


    # Group -- NODOCS -- Printing

    # Function -- NODOCS -- print
    # 
    # The ~print~ method deep-prints this object's properties in a format and
    # manner governed by the given ~printer~ argument; if the ~printer~ argument
    # is not provided, the global <uvm_default_printer> is used. See 
    # <uvm_printer> for more information on printer output formatting. See also
    # <uvm_line_printer>, <uvm_tree_printer>, and <uvm_table_printer> for details
    # on the pre-defined printer "policies," or formatters, provided by the UVM.
    #
    # The ~print~ method is not virtual and must not be overloaded. To include
    # custom information in the ~print~ and <sprint> operations, derived classes
    # must override the <do_print> method and use the provided printer policy
    # class to format the output.

    # @uvm-ieee 1800.2-2017 auto 5.3.6.1
    def print(self, printer=None):
        if printer is None:
            printer = uvm_printer.get_default()
        # TODO:
        printer.get_file().write(self.sprint(printer)); 


    # Function -- NODOCS -- sprint
    #
    # The ~sprint~ method works just like the <print> method, except the output
    # is returned in a string rather than displayed. 
    #
    # The ~sprint~ method is not virtual and must not be overloaded. To include
    # additional fields in the <print> and ~sprint~ operation, derived classes
    # must override the <do_print> method and use the provided printer policy
    # class to format the output. The printer policy will manage all string
    # concatenations and provide the string to ~sprint~ to return to the caller.

    # @uvm-ieee 1800.2-2017 auto 5.3.6.2
    def sprint(self, printer=None):
        if printer is None:
            printer = uvm_printer.get_default()
        if printer.get_active_object_depth() == 0:
            printer.flush()
            if printer.get_root_enabled():
                name = self.get_full_name()
            else:
                name = self.get_name()
        else:
            name = self.get_name()
            
        printer.print_object(name, self)
        
        return printer.emit()


    # Function -- NODOCS -- do_print
    #
    # The ~do_print~ method is the user-definable hook called by <print> and
    # <sprint> that allows users to customize what gets printed or sprinted 
    # beyond the field information provided by the `uvm_field_* macros,
    # <Utility and Field Macros for Components and Objects>.
    #
    # The ~printer~ argument is the policy object that governs the format and
    # content of the output. To ensure correct <print> and <sprint> operation,
    # and to ensure a consistent output format, the ~printer~ must be used
    # by all <do_print> implementations. That is, instead of using ~$display~ or
    # string concatenations directly, a ~do_print~ implementation must call
    # through the ~printer's~ API to add information to be printed or sprinted.
    #
    # An example implementation of ~do_print~ is as follows:
    #
    #| class mytype (uvm_object):;
    #|   data_obj data;
    #|   int f1;
    #|   virtual function void do_print (uvm_printer printer);
    #|     super.do_print(printer);
    #|     printer.print_field_int("f1", f1, $bits(f1), UVM_DEC);
    #|     printer.print_object("data", data);
    #|   endfunction
    #
    # Then, to print and sprint the object, you could write:
    #
    #| mytype t = new;
    #| t.print();
    #| uvm_report_info("Received",t.sprint());
    #
    # See <uvm_printer> for information about the printer API.

    # @uvm-ieee 1800.2-2017 auto 5.3.6.3
    def do_print(self, printer):
        pass


    # Function -- NODOCS -- convert2string
    #
    # This virtual function is a user-definable hook, called directly by the
    # user, that allows users to provide object information in the form of
    # a string. Unlike <sprint>, there is no requirement to use a <uvm_printer>
    # policy object. As such, the format and content of the output is fully
    # customizable, which may be suitable for applications not requiring the
    # consistent formatting offered by the <print>/<sprint>/<do_print>
    # API.
    #
    # Fields declared in <Utility Macros> macros (`uvm_field_*), if used, will
    # not automatically appear in calls to convert2string.
    #
    # An example implementation of convert2string follows.
    # 
    #| class base (uvm_object):;
    #|   string field = "foo";
    #|   virtual function string convert2string();
    #|     convert2string = {"base_field=",field};
    #|   endfunction
    #| endclass
    #| 
    #| class obj2 (uvm_object):;
    #|   string field = "bar";
    #|   virtual function string convert2string();
    #|     convert2string = {"child_field=",field};
    #|   endfunction
    #| endclass
    #| 
    #| class obj (base):;
    #|   int addr = 'h123;
    #|   int data = 'h456;
    #|   bit write = 1;
    #|   obj2 child = new;
    #|   virtual function string convert2string();
    #|      convert2string = {super.convert2string(),
    #|        $sformatf(" write=%0d addr=%8h data=%8h ",write,addr,data),
    #|        child.convert2string()};
    #|   endfunction
    #| endclass
    #
    # Then, to display an object, you could write:
    #
    #| obj o = new;
    #| uvm_report_info("BusMaster",{"Sending:\n ",o.convert2string()});
    #
    # The output will look similar to:
    #
    #| UVM_INFO @ 0: reporter [BusMaster] Sending:
    #|    base_field=foo write=1 addr=00000123 data=00000456 child_field=bar


    # @uvm-ieee 1800.2-2017 auto 5.3.6.4
    def convert2string(self):
        return ""


    # Group -- NODOCS -- Recording

    # Function -- NODOCS -- record
    #
    # The ~record~ method deep-records this object's properties according to an
    # optional ~recorder~ policy. The method is not virtual and must not be
    # overloaded. To include additional fields in the record operation, derived
    # classes should override the <do_record> method.
    #
    # The optional ~recorder~ argument specifies the recording policy, which
    # governs how recording takes place. See
    # <uvm_recorder> for information.
    #
    # A simulator's recording mechanism is vendor-specific. By providing access
    # via a common interface, the uvm_recorder policy provides vendor-independent
    # access to a simulator's recording capabilities.

    # @uvm-ieee 1800.2-2017 auto 5.3.7.1
    def record(self,recorder=None):
        if recorder is None:
            return
        
        recorder.record_object(self.get_name(), self)


    # Function -- NODOCS -- do_record
    #
    # The ~do_record~ method is the user-definable hook called by the <record>
    # method. A derived class should override this method to include its fields
    # in a record operation.
    #
    # The ~recorder~ argument is policy object for recording this object. A
    # do_record implementation should call the appropriate recorder methods for
    # each of its fields. Vendor-specific recording implementations are
    # encapsulated in the ~recorder~ policy, thereby insulating user-code from
    # vendor-specific behavior. See <uvm_recorder> for more information.
    #
    # A typical implementation is as follows:
    #
    #| class mytype (uvm_object):;
    #|   data_obj data;
    #|   int f1;
    #|   function void do_record (uvm_recorder recorder);
    #|     recorder.record_field("f1", f1, $bits(f1), UVM_DEC);
    #|     recorder.record_object("data", data);
    #|   endfunction

    # @uvm-ieee 1800.2-2017 auto 5.3.7.2
    def do_record(self, recorder):
        pass

    # Group -- NODOCS -- Copying

    # Function -- NODOCS -- copy
    #
    # The copy makes this object a copy of the specified object.
    #
    # The ~copy~ method is not virtual and should not be overloaded in derived
    # classes. To copy the fields of a derived class, that class should override
    # the <do_copy> method.

    # @uvm-ieee 1800.2-2017 auto 5.3.8.1
    def copy(self, rhs, copier=None):
        if rhs is None:
            # TODO: error handling
            # $fwrite(printer.get_file(),sprint(printer)); 
            return
        
        if copier is None:
            coreservice = uvm_coreservice_t.get()
            m_copier = coreservice.get_default_copier()
        else:
            m_copier = copier
            
            if m_copier.get_active_object_depth() == 0:
                m_copier.flush()
        
        m_copier.copy_object(self, rhs)

    # Function -- NODOCS -- do_copy
    #
    # The ~do_copy~ method is the user-definable hook called by the <copy> method.
    # A derived class should override this method to include its fields in a <copy>
    # operation.
    #
    # A typical implementation is as follows:
    #
    #|  class mytype (uvm_object):;
    #|    ...
    #|    int f1;
    #|    function void do_copy (uvm_object rhs);
    #|      mytype rhs_;
    #|      super.do_copy(rhs);
    #|      $cast(rhs_,rhs);
    #|      field_1 = rhs_.field_1;
    #|    endfunction
    #
    # The implementation must call ~super.do_copy~, and it must $cast the rhs
    # argument to the derived type before copying. 

    # @uvm-ieee 1800.2-2017 auto 5.3.8.2
    def do_copy(self, rhs):
        pass


    # Group -- NODOCS -- Comparing

    # Function -- NODOCS -- compare
    #
    # Deep compares members of this data object with those of the object provided
    # in the ~rhs~ (right-hand side) argument, returning 1 on a match, 0 otherwise.
    #
    # The ~compare~ method is not virtual and should not be overloaded in derived
    # classes. To compare the fields of a derived class, that class should
    # override the <do_compare> method.
    #
    # The optional ~comparer~ argument specifies the comparison policy. It allows
    # you to control some aspects of the comparison operation. It also stores the
    # results of the comparison, such as field-by-field miscompare information
    # and the total number of miscompares. If a compare policy is not provided,
    # then the global ~uvm_default_comparer~ policy is used. See <uvm_comparer> 
    # for more information.

    # @uvm-ieee 1800.2-2017 auto 5.3.9.1
    def compare(self, rhs, comparer=None):
        if comparer is None:
            comparer = uvm_comparer.get_default()
            
        if comparer.get_active_object_depth() == 0:
            comparer.flush()
        return comparer.compare_object(self.get_name(), self, rhs)


    # Function -- NODOCS -- do_compare
    #
    # The ~do_compare~ method is the user-definable hook called by the <compare>
    # method. A derived class should override this method to include its fields
    # in a compare operation. It should return 1 if the comparison succeeds, 0
    # otherwise.
    #
    # A typical implementation is as follows:
    #
    #|  class mytype (uvm_object):;
    #|    ...
    #|    int f1;
    #|    virtual function bit do_compare (uvm_object rhs,uvm_comparer comparer);
    #|      mytype rhs_;
    #|      do_compare = super.do_compare(rhs,comparer);
    #|      $cast(rhs_,rhs);
    #|      do_compare &= comparer.compare_field_int("f1", f1, rhs_.f1);
    #|    endfunction
    #
    # A derived class implementation must call ~super.do_compare()~ to ensure its
    # base class' properties, if any, are included in the comparison. Also, the
    # rhs argument is provided as a generic uvm_object. Thus, you must ~$cast~ it
    # to the type of this object before comparing. 
    #
    # The actual comparison should be implemented using the uvm_comparer object
    # rather than direct field-by-field comparison. This enables users of your
    # class to customize how comparisons are performed and how much miscompare
    # information is collected. See uvm_comparer for more details.

    # @uvm-ieee 1800.2-2017 auto 5.3.9.2
    def do_compare(self, rhs, comparer):
        return True

    # Group -- NODOCS -- Packing

    # Function -- NODOCS -- pack

    # @uvm-ieee 1800.2-2017 auto 5.3.10.1
    def pack(self, bitstream, packer=None):
        # TODO: m_pack uses inout for packer
        packer = self._m_pack(packer)
        packer.get_packed_bits(bitstream)
        return packer.get_packed_size()

    # Function -- NODOCS -- pack_bytes

    # @uvm-ieee 1800.2-2017 auto 5.3.10.1
    def pack_bytes(self, bytestream, packer=None):
        # TODO: m_pack uses inout for packer
        packer = self._m_pack(packer)
        packer.get_packed_bytes(bytestream)
        return packer.get_packed_size()

    # Function -- NODOCS -- pack_ints
    #
    # The pack methods bitwise-concatenate this object's properties into an array
    # of bits, bytes, or ints. The methods are not virtual and must not be
    # overloaded. To include additional fields in the pack operation, derived
    # classes should override the <do_pack> method.
    #
    # The optional ~packer~ argument specifies the packing policy, which governs
    # the packing operation. If a packer policy is not provided, the global
    # <uvm_default_packer> policy is used. See <uvm_packer> for more information.
    #
    # The return value is the total number of bits packed into the given array.
    # Use the array's built-in ~size~ method to get the number of bytes or ints
    # consumed during the packing process.

    # @uvm-ieee 1800.2-2017 auto 5.3.10.1
    def pack_ints(self, intstream, packer=None):
        packer = self._m_pack(packer)
        packer.get_packed_ints(intstream)
        return packer.get_packed_size()
  
    # @uvm-ieee 1800.2-2017 auto 5.3.10.1
    def pack_longints(self, longintstream, packer=None):
        packer = self._m_pack(packer)
        packer.get_packed_longints(longintstream)
        return packer.get_packed_size()
  
  
    # Function -- NODOCS -- do_pack
    #
    # The ~do_pack~ method is the user-definable hook called by the <pack> methods.
    # A derived class should override this method to include its fields in a pack
    # operation.
    #
    # The ~packer~ argument is the policy object for packing. The policy object
    # should be used to pack objects. 
    #
    # A typical example of an object packing itself is as follows
    #
    #|  class mysubtype (mysupertype):;
    #|    ...
    #|    shortint myshort;
    #|    obj_type myobj;
    #|    byte myarray[];
    #|    ...
    #|    function void do_pack (uvm_packer packer);
    #|      super.do_pack(packer); # pack mysupertype properties
    #|      packer.pack_field_int(myarray.size(), 32);
    #|      foreach (myarray)
    #|        packer.pack_field_int(myarray[index], 8);
    #|      packer.pack_field_int(myshort, $bits(myshort));
    #|      packer.pack_object(myobj);
    #|    endfunction
    #
    # The implementation must call ~super.do_pack~ so that base class properties
    # are packed as well.
    #
    # If your object contains dynamic data (object, string, queue, dynamic array,
    # or associative array), and you intend to unpack into an equivalent data
    # structure when unpacking, you must include meta-information about the
    # dynamic data when packing as follows.
    #
    #  - For queues, dynamic arrays, or associative arrays, pack the number of
    #    elements in the array in the 32 bits immediately before packing
    #    individual elements, as shown above.
    #
    #  - For string data types, append a zero byte after packing the string
    #    contents.
    #
    #  - For objects, pack 4 bits immediately before packing the object. For ~null~
    #    objects, pack 4'b0000. For non-~null~ objects, pack 4'b0001.
    #
    # When the `uvm_field_* macros are used, 
    # <Utility and Field Macros for Components and Objects>,
    # the above meta information is included.
    #
    # Packing order does not need to match declaration order. However, unpacking
    # order must match packing order.

    # @uvm-ieee 1800.2-2017 auto 5.3.10.2
    def do_pack (self, packer):
        if packer is None:
            # TODO: error handling
            # `uvm_error("UVM/OBJ/PACK/NULL", "uvm_object::do_pack called with null packer!")
            pass

    # Group -- NODOCS -- Unpacking

    # Function -- NODOCS -- unpack

    # @uvm-ieee 1800.2-2017 auto 5.3.11.1
    def unpack (self, bitstream, packer=None):
        packer = self.m_unpack_pre(packer)
        packer.set_packed_bits(bitstream)
        return self.m_unpack_post(packer)

    # Function -- NODOCS -- unpack_bytes

    # @uvm-ieee 1800.2-2017 auto 5.3.11.1
    def unpack_bytes (self, bytestream, packer=None):
        packer = self.m_unpack_pre(packer)
        packer.set_packed_bytes(bytestream)
        return self.m_unpack_post(packer)
  
    # Function -- NODOCS -- unpack_ints
    #
    # The unpack methods extract property values from an array of bits, bytes, or
    # ints. The method of unpacking ~must~ exactly correspond to the method of
    # packing. This is assured if (a) the same ~packer~ policy is used to pack
    # and unpack, and (b) the order of unpacking is the same as the order of
    # packing used to create the input array.
    #
    # The unpack methods are fixed (non-virtual) entry points that are directly
    # callable by the user. To include additional fields in the <unpack>
    # operation, derived classes should override the <do_unpack> method.
    #
    # The optional ~packer~ argument specifies the packing policy, which governs
    # both the pack and unpack operation. If a packer policy is not provided,
    # then the global ~uvm_default_packer~ policy is used. See uvm_packer for
    # more information.
    #
    # The return value is the actual number of bits unpacked from the given array.
  
    # @uvm-ieee 1800.2-2017 auto 5.3.11.1
    def unpack_ints(self, intstream, packer=None):
        packer = self.m_unpack_pre(packer)
        packer.set_packed_ints(intstream)
        return self.m_unpack_post(packer)

    # @uvm-ieee 1800.2-2017 auto 5.3.11.1
    def unpack_longints(self, longintstream, packer=None):
        packer = self.m_unpack_pre(packer)
        packer.set_packed_longints(longintstream)
        return self.m_unpack_post(packer)


    # Function -- NODOCS -- do_unpack
    #
    # The ~do_unpack~ method is the user-definable hook called by the <unpack>
    # method. A derived class should override this method to include its fields
    # in an unpack operation.
    #
    # The ~packer~ argument is the policy object for both packing and unpacking.
    # It must be the same packer used to pack the object into bits. Also,
    # do_unpack must unpack fields in the same order in which they were packed.
    # See <uvm_packer> for more information.
    #
    # The following implementation corresponds to the example given in do_pack.
    #
    #|  function void do_unpack (uvm_packer packer);
    #|   int sz;
    #|    super.do_unpack(packer); # unpack super's properties
    #|    sz = packer.unpack_field_int(myarray.size(), 32);
    #|    myarray.delete();
    #|    for(int index=0; index<sz; index++)
    #|      myarray[index] = packer.unpack_field_int(8);
    #|    myshort = packer.unpack_field_int($bits(myshort));
    #|    packer.unpack_object(myobj);
    #|  endfunction
    #
    # If your object contains dynamic data (object, string, queue, dynamic array,
    # or associative array), and you intend to <unpack> into an equivalent data
    # structure, you must have included meta-information about the dynamic data
    # when it was packed. 
    #
    # - For queues, dynamic arrays, or associative arrays, unpack the number of
    #   elements in the array from the 32 bits immediately before unpacking
    #   individual elements, as shown above.
    #
    # - For string data types, unpack into the new string until a ~null~ byte is
    #   encountered.
    #
    # - For objects, unpack 4 bits into a byte or int variable. If the value
    #   is 0, the target object should be set to ~null~ and unpacking continues to
    #   the next property, if any. If the least significant bit is 1, then the
    #   target object should be allocated and its properties unpacked.

    # @uvm-ieee 1800.2-2017 auto 5.3.11.2
    def do_unpack(self, packer):
        if packer is None:
            # TODO: error handling
            # `uvm_error("UVM/OBJ/UNPACK/NULL", "uvm_object::do_unpack called with null packer!")
            pass

    # @uvm-ieee 1800.2-2017 auto 5.3.13.1
    def do_execute_op(self, op):
        pass


    # Group -- NODOCS -- Configuration
 
    # @uvm-ieee 1800.2-2017 auto 5.3.12
    def set_local(self,rsrc):
        if rsrc is None:
            return
        else:
            op = uvm_field_op.m_get_available_op()
            op.set(UVM_SET, None, rsrc)
            self.do_execute_op(op)
            op.m_recycle()

    #---------------------------------------------------------------------------
    #                 **** Internal Methods and Properties ***
    #                           Do not use directly
    #---------------------------------------------------------------------------

    def _m_pack(self, packer):
        if packer is None:
            packer = uvm_packer.get_default()
        
        if packer.get_active_object_depth() == 0:
            packer.flush()
        packer.pack_object(self)
        
        return packer

    def m_unpack_pre (self, packer):
        if packer is None:
            packer = uvm_packer.get_default()
        
        if packer.get_active_object_depth() == 0:
            packer.flush()
            
        return packer
    
    def m_unpack_post(self, packer):
        size_before_unpack = packer.get_packed_size()
        packer.unpack_object(self)
        return size_before_unpack - packer.get_packed_size()
    
    def m_unsupported_set_local(self, rsrc):
        pass

    # The print_matches bit causes an informative message to be printed
    # when a field is set using one of the set methods.

    def __m_uvm_field_automation (self, tmp_data__,  what__, str__):
        pass

    def m_get_report_object(self):
        return None


